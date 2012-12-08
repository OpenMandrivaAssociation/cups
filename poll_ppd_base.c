/*
 *
 *   poll_ppd_base
 *   -------------
 #
 #   A simple tool for getting a list of all installed PPD files
 #   with printer manufacturer and printer model, polling the database
 #   of the CUPS daemon. This program is mainly intended to be called
 #   from installation/configuration scripts for CUPS.
 #
 #   ONLY WORKS WITH CUPS DAEMON RUNNING!
 #   The CUPS library (libcups.so.*) must be installed!
 #
 #   Compile with: gcc -opoll_ppd_base -lcups poll_ppd_base.c
 #
 *   Copyright 2000 by Till Kamppeter
 *
 *   This program is free software; you can redistribute it and/or
 *   modify it under the terms of the GNU General Public License as
 *   published by the Free Software Foundation; either version 2 of the
 *   License, or (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
 *   02111-1307  USA
 *
 */

/*
 * Include necessary headers...
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <cups/cups.h>
#include <cups/ipp.h>
#include <cups/language.h>

// IPP Request routines for getting the printer type, stolen from QTCUPS from
// Michael Goffioul (file qtcups/cupshelper.cpp)

ipp_t* newIppRequest()
{
  ipp_t *request;
  cups_lang_t *lang;
  request = ippNew();
  request->request.op.request_id = 1;
  lang = cupsLangDefault();
  ippAddString(request,IPP_TAG_OPERATION,IPP_TAG_CHARSET,"attributes-charset",NULL,cupsLangEncoding(lang));
  ippAddString(request,IPP_TAG_OPERATION,IPP_TAG_LANGUAGE,"attributes-natural-language",NULL,lang->language);
  return request;
} 

ipp_t* processRequest(ipp_t *req, const char *res)
{
  http_t  *HTTP;
  ipp_t   *answer;
  HTTP = httpConnect(cupsServer(),ippPort());
  if (!HTTP) {
    ippDelete(req);
    return 0;
  }
  answer = cupsDoRequest(HTTP,req,res);
  httpClose(HTTP);
  if (!answer) return 0;
  if (answer->state == IPP_ERROR || answer->state == IPP_IDLE) {
    ippDelete(answer);
    return 0;
  }
  return answer;
} 

ipp_t *getPPDList()
{
  ipp_t       *request = newIppRequest();
  char        str[1024];
  const char* server = cupsServer();
  int         port = ippPort();

  request->request.op.operation_id = CUPS_GET_PPDS;
  if ((!server) || (port < 0)) return NULL;
  sprintf(str,"ipp://%s:%d/printers/",cupsServer(),ippPort());
  ippAddString(request,IPP_TAG_OPERATION,IPP_TAG_URI,"printer-uri",NULL,str);
  //str.sprintf("/printers/%s",name);
  request = processRequest(request,"/");
  return request;
} 

/*
 *  Main program
 */

int                 /* O - exit state */
main(int  argc,     /* I - Number of command-line arguments */
     char *argv[])  /* I - Command-line arguments */
{
  int		i,j;		/* Looping vars */
  int           makelen = 0;    /* Length of current manufacturer name */
  int           makelist = 0;   /* List of manufacturers */
  int           makegiven = 0;  /* List of models for given manufacturer */
  int           all = 0;        /* LIst of all models */
  char          *make;          /* Chosen manufacturer */
  ipp_t         *ppdlist;       /* List of PPD files resulting from IPP */
                                /* request */
  ipp_attribute_t *attr,        /* Current attribute */
                *last;          /* Last attribute */
  char          *currmake,      /* current data read from PPD list */
                *currmod,
                *currlang,
                *currfile,
                *currid,
                *c;
  char          buffer[80],
                buffer2[256];
  int           lineprinted = 1; /* Is the current line already printed to
                                    stdout */
  
  // read command line arguments

  for (i = 1; i < argc; i ++)
    if (argv[i][0] == '-') {
      switch (argv[i][1]) {
	case 'm' : /* Manufacturer options */
          if (argv[i][2] != '\0') {
            if (strcmp(argv[i],"-ml") == 0) {
              makelist = 1;
            } else {
              make = argv[i] + 2;
              makegiven = 1;
            }              
          } else {
            i ++;
            if (!(make = argv[i])) return 1;
            makegiven = 1;              
          }
          break;
        case 'a' : /* List all PPD files */
          all = 1;
          break;
	default :
          fprintf(stderr,"Unknown option \'%c\'!\n", argv[i][1]);
          fprintf(stderr,"Start program without options for help!\n");
          return(1);
      }
    } else {
      fprintf(stderr,"Unknown option \'%s\'!", argv[i]);
      fprintf(stderr,"Start program without options for help!\n");
      return(1);
    }
  if ((all) || (makegiven)) { // list all PPDs or PPDs of given manufacturer
    ppdlist = getPPDList();
    if (!ppdlist) return 1;
    for (attr = ppdlist->attrs; // go through all entries
         attr != NULL;
         attr = attr->next)
      if (attr->name) {
        // read data items
        if (strcmp(attr->name, "ppd-name") == 0) {
	  currfile = attr->values[0].string.text;
          lineprinted = 0;
        } else if (strcmp(attr->name, "ppd-make") == 0) {
          currmake = attr->values[0].string.text;
        } else if (strcmp(attr->name, "ppd-make-and-model") == 0) {
          currmod = attr->values[0].string.text;
        } else if (strcmp(attr->name, "ppd-natural-language") == 0) {
          currlang = attr->values[0].string.text;
        } else if (strcmp(attr->name, "ppd-device-id") == 0) {
          currid = attr->values[0].string.text;
        }
      } else { // attr->name = NULL ==> data set completed
        lineprinted = 1;
        // Fill empty entries with some default stuff
        if (!currmod) currmod = "UNKNOWN";
        if (!currmake) currmake = "UNKNOWN";
        if (!currlang) currlang = "en";
        // Put data to stdout when "all" is chosen or when the manufacturer
        // matches the given one.
        if ((currfile) && ((all) || !strcasecmp(currmake,make))) {
	  if (currid && (currid[0]))
	    printf("%s|%s|%s|%s|%s\n",currfile,currmake,currmod,currlang,
		   currid);
	  else
	    printf("%s|%s|%s|%s\n",currfile,currmake,currmod,currlang);
	}
	currfile = NULL; currmake = NULL; currmod = NULL;
	currlang = NULL; currid = NULL;
      }
    if (!lineprinted) {
      // Fill empty entries with some default stuff
      if (!currmod) currmod = "UNKNOWN";
      if (!currmake) currmake = "UNKNOWN";
      if (!currlang) currlang = "en";
      // Put data to stdout when "all" is chosen or when the manufacturer
      // matches the given one.
      if ((currfile) && ((all) || !strcasecmp(currmake,make))) {
	if (currid && (currid[0]))
	  printf("%s|%s|%s|%s|%s\n",currfile,currmake,currmod,currlang,
		 currid);
	else
	  printf("%s|%s|%s|%s\n",currfile,currmake,currmod,currlang);
      }
    }
  } else if (makelist) { // list all manufacturers
    ppdlist = getPPDList(); 
    if (!ppdlist) return 1;
    for (attr = ppdlist->attrs, last = NULL; // go through all entries
         attr != NULL;
         attr = attr->next)
      if (attr->name && strcmp(attr->name, "ppd-make") == 0)
	                    // only search for manufacturerer entriees
        if (last == NULL ||
            strcasecmp(last->values[0].string.text,
                       attr->values[0].string.text) != 0)
	                    // Do not take the same manufacturer twice
          {
            // Put found manufacturer to stdout
            printf("%s\n",attr->values[0].string.text);
            last = attr;
          }
  } else { // Help!
    fprintf(stderr,"Usage:\n");
    fprintf(stderr,"------\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"   poll_ppd_base\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"      This help page\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"   poll_ppd_base -a\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"      List all PPD files\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"   poll_ppd_base -ml\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"      List of all printer manufacturers supported by the PPD files installed\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"   poll_ppd_base -m <manufacturers name>\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"      List of all supported printer models of this manufacturer\n");
    fprintf(stderr,"\n");
    fprintf(stderr,"ONLY WORKS WITH CUPS DAEMON RUNNING!\n");
    fprintf(stderr,"\n");
    return(1);
  }
  return(0);
}
