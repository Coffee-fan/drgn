#include <syslog.h>

void set_logfile(char *logfile);
void log_print(char *filename, const char *function, int line, int log_level, char *fmt, ...);

// #define LOG_PRINT(...) log_print(__FILE__, __LINE__, __VA_ARGS__ )
#define LOGGER(log_level, ...) log_print(__FILE__, __FUNCTION__, __LINE__, log_level, __VA_ARGS__ )
#define LOGGER_INFO(...) log_print(__FILE__, __FUNCTION__, __LINE__, LOG_INFO, __VA_ARGS__ )
#define LOGGER_WARN(...) log_print(__FILE__, __FUNCTION__, __LINE__, LOG_WARNING, __VA_ARGS__ )
