
/*

    This C source file is for compiling into the sample program
    APISAMPLE.PGM.  It invokes the configuration file APIs
    contained in SRVPGM QHTTPSVR/QZHBCONF to read in
    a configuration file, and either replace an existing PORT
    directive or to add a new one.

    This code is written by IBM, and is intended only as a sample.
    There is no implied support for this code, and it is not
    a part of any IBM product.  It can be freely copied, modified
    and used in any way desired.

*/


#include <stdio.h>
#include <stdlib.h>

#include <qusec.h>      /* For errcode structure */
#include <qzhbconf.h>   /* For group file API's */

int main (int argc, char **argv)
{
    Qus_EC_t errcode;               /* Error code structure */
    unsigned char configname10[10]; /* Config name */
    unsigned int cfghdl;            /* Handle for config file */
    unsigned int getlock = 1;       /* Argument to request a write lock */
    unsigned char valstr[100];      /* Value string argument */
    unsigned int vallen;            /* Length argument */
    unsigned int numtofind = 0;     /* Will be searching for last directive */
    unsigned int casesense = 0;     /* Case insensitive search */
    unsigned int writecfg = 1;      /* Write config back out */
    unsigned int dirhdl;            /* Handle for a directive */

    if (argc <= 2 || strlen(argv[1]) > 10 || atoi(argv[2]) < 1) {
        printf("usage:  call lib/prog 'configname' 'portnumber'\n");
        return 1;
    }

    /* Get config name into a 10 character format */
    strncpy((char *) configname10, "          ", 10);
    strncpy((char *) configname10, argv[1], strlen(argv[1]));

    /* Set up error code structure */
    errcode.Bytes_Provided = sizeof(Qus_EC_t);

    /* Open the config - program will end if error occurs */
    QzhbOpenConfig(configname10, &getlock, &cfghdl, NULL);

    /* Search for the last PORT directive in the file */
    strcpy((char *) valstr, "port");
    vallen = strlen((char *) valstr);
    QzhbFindDirective(&cfghdl, valstr, &vallen, NULL,
                      &numtofind, &casesense, &dirhdl,
                     (unsigned char *) &errcode);

    /* Build string containing what we want the PORT directive to look like */
    sprintf((char *) valstr, "Port %s", argv[2]);
    vallen = strlen((char *) valstr);

    /* If found a PORT directive, replace it with our new value */
    if (errcode.Bytes_Available == 0) {
	/* Replace existing directive, letting error end the program */
        QzhbReplaceDirective(&cfghdl, &dirhdl,
                             valstr, &vallen, NULL);
        printf("Replaced existing PORT directive in configuration %s with: %s\n",
               argv[1], valstr);
    }

    /* If did not find the PORT directive, we want to add a new one */
    else {
        unsigned int insertpos = 4;  /* Automatic positioning */
	/* Add new directive, letting error end the program */
        QzhbAddDirective(&cfghdl, valstr, &vallen,
                         &insertpos, NULL, &dirhdl, NULL);
        printf("Added new PORT directive in configuration %s as: %s\n",
               argv[1], valstr);
    }