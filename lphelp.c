/*
 *
 *   lphelp
 *   ------
 #
 #   A simple tool for getting information about an installed printer or a
 #   PPD file. Especially the printer-specific options defined in the PPD
 #   file are listed, so that one can make use of them with the "lp", "lpr",
 #   and "lpoptions" commands. The programm can also be used by installation/
 #   configuration scripts to give a "preview" to a PPD file.
 #
 #   ONLY WORKS WITH CUPS DAEMON RUNNING!
 #   The CUPS library (libcups.so.*) must be installed!
 #
 #   Compile with: gcc -olphelp -lcups lphelp.c
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

#include <cups/cups.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

/*
 * 'main()' - Main entry for test program.
 */

int				/* O - Exit status */
main(int  argc,			/* I - Number of command-line arguments */
     char *argv[])		/* I - Command-line arguments */
{
  int		i, j, k, m;	/* Looping vars */
  const char	*filename;	/* File to load */
  FILE          *ppdfile;

  // Temporary file name (for reading from stdin)
  char          tmpfile[19] = "/tmp/lphelp.XXXXXX";
  const int     blocksize = 1024;
  char          buffer[blocksize];
  int           bytesread;

  // variables for parsing PPD file for usual options (boolean, enumerated)
  ppd_file_t	*ppd;		/* PPD file record */
  ppd_size_t	*size;		/* Size record */
  ppd_group_t	*group;		/* UI group */
  ppd_option_t	*option;	/* Standard UI option */
  ppd_choice_t	*choice;	/* Standard UI option choice */
  static char	*uis[] = { "BOOLEAN", "PICKONE", "PICKMANY" };
  static char	*sections[] = { "ANY", "DOCUMENT", "EXIT",
                                "JCL", "PAGE", "PROLOG" };

  // variables for parsing CUPS-O-MATIC info for numerical options (float, int)
  char line[1024], /* buffer for reading PPD file line by
                      line to search numerical options */
       item[1024], /* item to be defined (left of "=>") */
       value[1024], /* value for item (right of "=>") */
       argname[1024], /* name of the current argument */
       comment[1024]; /* human-readable argument name */
  const char *line_contents; /* contents of line */
  const char *scan; /* pointer scanning the line */
  char *writepointer;
  double min, max, defvalue; /* Range of numerical 
                                CUPS-O-MATIC option */
  int opttype; /* 0 = other, 1 = int, 2 = float */
  int openbrackets; /* How many curled brackets are open? */
  int inquotes; /* are we in quotes now? */
  int inargspart; /* are we in the arguments part now? */
       
 /*
  * Display PPD files for each file listed on the command-line...
  */

  if (argc == 1) {
    fputs("Usage: lphelp <filename1>.ppd [<filename2>.ppd ...]\n       lphelp <printername1> [<printername2> ...]\n       lphelp -\n", stderr);
      return (1);
  }

  for (i = 1; i < argc; i ++) {
    if ((strstr(argv[i], ".ppd")) || (strstr(argv[i], "-")))
      filename = argv[i];
    else
      filename = cupsGetPPD(argv[i]);
    if (strcmp(filename,"-") == 0) {
      if ((ppdfile = fdopen(mkstemp(tmpfile), "w")) == NULL) {
	fprintf(stderr, "Unable to generate temporary file!\n");
      }
      while ((bytesread = fread(buffer, 1, blocksize, stdin)) > 0) {
	fwrite(buffer, 1, bytesread, ppdfile);
      }
      fclose(ppdfile);
      filename = tmpfile;
    }
    if ((ppd = ppdOpenFile(filename)) == NULL) {
      fprintf(stderr, "Unable to open \'%s\' as a PPD file!\n", filename);
      continue;
    }

    printf("==============================================================================\n\n");
    printf("%s\n\n", ppd->modelname);
    printf("==============================================================================\n\n");
    printf("   %s printer\n\n", ppd->color_device ? "Colour" : "Black & white");
    printf("   Printer-specific options\n");
    printf("   ------------------------\n\n");
    printf("   Besides the options described in the CUPS software users manual\n"); 
    printf("   (http://localhost:631/sum.html) you can use also the following options\n");
    printf("   when you print on this printer with the \"lp\" or \"lpr\" command (a choice\n");
    printf("   with the \"default\" mark represents the behaviour of the printer when the\n");
    printf("   appropriate option is not given on the command line):\n\n");

    for (j = 0, group = ppd->groups; j < ppd->num_groups; j ++, group ++) {
      for (k = 0, option = group->options; k < group->num_options;
           k ++, option ++) {
        if (strcmp(option->keyword, "PageRegion") != 0) {
          if ((strcmp(uis[option->ui],"BOOLEAN") == 0) || 
              (strcmp(uis[option->ui],"PICKONE") == 0)) {  
	    printf("   %s:  -o %s=<choice>\n\n",
	           option->text, option->keyword);
            printf("      <choice> can be one of the following:\n\n");
          } else {
	    printf("   %s:  -o %s=<choice1>,<choice2>,...\n\n",
	           option->text, option->keyword);
            printf("      <choice1>, <choice2>, and so on can be out of the following:\n\n");
          }
          if (strcmp(option->keyword, "PageSize") == 0) {
            for (m = option->num_choices, choice = option->choices;
	         m > 0;
	         m --, choice ++) {
	      size = ppdPageSize(ppd, choice->choice);

	      if (size == NULL)
	        printf("      %s  (%s, size unknown", choice->choice, choice->text);
              else
	        printf("      %s  (%s, size: %.2fx%.2fin", choice->choice,
	               choice->text, size->width / 72.0, size->length / 72.0);
              if (strcmp(option->defchoice, choice->choice) == 0)
	        puts(", default)");
	      else
	        puts(")");
            }
	  } else {
	    for (m = option->num_choices, choice = option->choices;
	         m > 0;
	         m --, choice ++) {
	      printf("      %s  (%s", choice->choice, choice->text);
              if (strcmp(option->defchoice, choice->choice) == 0)
	        puts(", default)");
	      else
	        puts(")");
	    }
          }
          printf("\n");
        }
      }
    }
    ppdClose(ppd);

    // Search for numerical options of CUPS-O-MATIC
    if ((ppdfile = fopen(filename,"r")) == NULL) {
      fprintf(stderr, "Unable to open \'%s\' as a PPD file!\n", filename);
      continue;
    }
    // Reset all variables
    opttype = 0;
    min = 0.0; max = 0.0; defvalue = 0.0;
    openbrackets = 0;
    inquotes = 0;
    writepointer = item;
    inargspart = 0;
    // Read the PPD file again, line by line.
    while (fgets(line,sizeof(line),ppdfile)) {
      // evaluate only lines with CUPS-O-MATIC info
      if (line_contents = strstr(line,"*% COMDATA #")) {
        line_contents += 12; // Go to the text after 
	                     // "*% COMDATA #"
        for (scan = line_contents; 
             (*scan != '\n') && (*scan != '\0');
	     scan ++) {
          switch(*scan) {
	    case '[': // open square bracket
	    case '{': // open curled bracket
              if (!inquotes) {
                openbrackets ++;
                // we are on the left hand side now
                *writepointer = '\0';
                writepointer = item;
                // in which type of block are we now?
                if ((openbrackets == 2) && 
                    (strncasecmp(item,"args",4) == 0)) {
                  // we are entering the arguments section now
                  inargspart = 1;
		}
                if ((openbrackets == 3) && 
                    (inargspart == 1)) {
                  // new argument, get its name
                  strcpy(argname,item);
		}
                // item already evaluated now
                item[0] = '\0';
              } else {*writepointer = *scan; writepointer ++;}
              break;
	    case ',': // end of logical line
	    case ']': // close square bracket
	    case '}': // close curled bracket
              if (!inquotes) {
                // right hand side completed, go to left hand side
                *writepointer = '\0';
                writepointer = item;
                // evaluate logical line
                if (item[0]) {
                  // Machine-readable argument name
                  if ((openbrackets == 3) &&
                      (inargspart == 1) &&
                      (strcasecmp(item,"name") == 0)) {
                    strcpy(argname,value);
		  }
                  // Human-readable argument name
                  if ((openbrackets == 3) &&
                      (inargspart == 1) &&
                      (strcasecmp(item,"comment") == 0)) {
                    strcpy(comment,value);
		  }
                  // argument type
                  if ((openbrackets == 3) &&
                      (inargspart == 1) &&
                      (strcasecmp(item,"type") == 0)) {
                    if (strcasecmp(value,"int") == 0) opttype = 1;
                    if (strcasecmp(value,"float") == 0) opttype = 2;
		  }
                  // minimum value
                  if ((openbrackets == 3) &&
                      (inargspart == 1) &&
                      (strcasecmp(item,"min") == 0)) {
                    min = atof(value);
		  }
                  // maximum value
                  if ((openbrackets == 3) &&
                      (inargspart == 1) &&
                      (strcasecmp(item,"max") == 0)) {
                    max = atof(value);
		  }
                  // default value
                  if ((openbrackets == 3) &&
                      (inargspart == 1) &&
                      (strcasecmp(item,"default") == 0)) {
                    defvalue = atof(value);
		  }
                  // item already evaluated now
                  item[0] = '\0';
                }
                // close bracket
                if ((*scan == '}') || (*scan == ']')) {
                  // which block did we complete now?
                  if ((openbrackets == 2) && 
                      (inargspart == 1)) {
                    // We are leaving the arguments part now
                    inargspart = 0;
                  }
                  if ((openbrackets == 3) && 
                      (inargspart == 1)) {
                    // The current option is completely parsed
                    // Is the option a valid numerical option?
                    if ((opttype > 0) &&
                        (min != max) &&
                        (argname[0])) {
                      // Correct the default value, if necessary
                      if (min < max) {
                        if (defvalue < min) defvalue = min;
                        if (defvalue > max) defvalue = max;
		      } else {
                        if (defvalue < max) defvalue = max;
                        if (defvalue > min) defvalue = min;
                      }
                      // Show the found argument
	              printf("   %s:  -o %s=<value>\n\n",
	                comment, argname);
                      if (opttype == 1) {
                        printf(
                          "      <value> must be an integer number in the range %d..%d\n",
                          (int)(min),(int)(max));
                        printf(
			  "      The default value is %d\n\n",
                          (int)(defvalue));
		      } else {
                        printf(
                          "      <value> must be a decimal number in the range %.2f..%.2f\n",
                          min,max);
                        printf(
			  "      The default value is %.2f\n\n",
                          defvalue);
                      }
                    }
                    // reset the values
                    argname[0] = '\0';
                    opttype = 0;
                    min = 0.0; max = 0.0; defvalue = 0.0;
                  }
                  openbrackets --;
                }
              } else {*writepointer = *scan; writepointer ++;}
              break;
	    case '\'': // quote
              if (!inquotes) { // open quote pair
                inquotes = 1;
	      } else { // close quote pair
                inquotes = 0;
              }
              break;
	    case '=': // "=>"
              if ((!inquotes) && (*(scan + 1) == '>')) {
                scan ++;
                // left hand side completed, go to right hand side
                *writepointer = '\0';
                writepointer = value;
              } else {*writepointer = *scan; writepointer ++;}
              break;
	    case ' ':  // white space
	    case '\t':
              if (!inquotes) {
                // ignore white space outside quotes
              } else {*writepointer = *scan; writepointer ++;}
              break;
	    default:
              // write all other characters
              *writepointer = *scan; writepointer ++;
              break;
          } 
        }
        inquotes = 0; // quote pairs cannot enclose more
	              // than one line
      }
    }
    fclose(ppdfile);
    printf("\n\n\n");
  }

  if (!(strstr(tmpfile, "XXXXXX"))) {
    unlink(tmpfile);
  }

  return (0);
}
