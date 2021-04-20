#include <stdio.h>
#include <stdarg.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
// Next one to share the log levels
#include "drgnlog.h"

FILE *m_fp = NULL;

static char *logLevels[] = {
    "EMERGENCY",
    "ALERT",
    "CRITICAL",
    "ERROR",
    "WARNING",
    "NOTICE",
    "INFO",
    "DEBUG"};

static void log_exit()
{
    LOGGER(LOG_DEBUG, "Calling log_exit");
    if (NULL != m_fp)
    {
        fclose(m_fp);
        m_fp = NULL;
    }
}

void set_logfile(char *logfile)
{
    if (NULL != logfile && '\0' != logfile[0] && NULL == m_fp)
    {
        m_fp = fopen(logfile, "a");
        atexit(log_exit);
        LOGGER(LOG_DEBUG, "Opened log file %s for writing", logfile);
    }
}

void log_print(char *filename, const char *function, int line, int log_level, char *fmt, ...)
{
    va_list list;
    char *p, *r;
    int e;

    if (NULL == m_fp)
    {
        set_logfile("log.txt");
    }
    time_t t = time(NULL); /* get current calendar time */

    char *timestr = asctime(localtime(&t));
    timestr[strlen(timestr) - 1] = 0; //Get rid of \n

    fprintf(m_fp, "%s ", timestr);
    fprintf(m_fp, "%s: ", logLevels[log_level]);
    fprintf(m_fp, "%s - %s: %d ", filename, function, line);
    va_start(list, fmt);

    for (p = fmt; *p; ++p)
    {
        if (*p != '%') //If simple string
        {
            fputc(*p, m_fp);
        }
        else
        {
            switch (*++p)
            {
                /* string */
            case 's':
            {
                r = va_arg(list, char *);

                fprintf(m_fp, "%s", r);
                continue;
            }

            /* integer */
            case 'd':
            {
                e = va_arg(list, int);

                fprintf(m_fp, "%d", e);
                continue;
            }

            default:
                fputc(*p, m_fp);
            }
        }
    }
    va_end(list);
    fputc('\n', m_fp);
    fflush(m_fp);
}