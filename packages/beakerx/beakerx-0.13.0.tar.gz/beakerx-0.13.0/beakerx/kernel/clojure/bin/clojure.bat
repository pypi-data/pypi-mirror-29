@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  clojure startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Add default JVM options here. You can also use JAVA_OPTS and CLOJURE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto init

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:init
@rem Get command-line arguments, handling Windows variants

if not "%OS%" == "Windows_NT" goto win9xME_args

:win9xME_args
@rem Slurp the command line arguments.
set CMD_LINE_ARGS=
set _SKIP=2

:win9xME_args_slurp
if "x%~1" == "x" goto execute

set CMD_LINE_ARGS=%*

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\clojure.jar;%APP_HOME%\lib\clojure-1.8.0.jar;%APP_HOME%\lib\pomegranate-0.3.1.jar;%APP_HOME%\lib\aether-api-1.13.1.jar;%APP_HOME%\lib\aether-util-1.13.1.jar;%APP_HOME%\lib\aether-impl-1.13.1.jar;%APP_HOME%\lib\aether-connector-file-1.13.1.jar;%APP_HOME%\lib\aether-connector-wagon-1.13.1.jar;%APP_HOME%\lib\maven-aether-provider-3.0.4.jar;%APP_HOME%\lib\dynapath-0.2.3.jar;%APP_HOME%\lib\wagon-provider-api-2.2.jar;%APP_HOME%\lib\wagon-http-2.2.jar;%APP_HOME%\lib\aether-spi-1.13.1.jar;%APP_HOME%\lib\plexus-classworlds-2.4.jar;%APP_HOME%\lib\sisu-inject-plexus-2.2.3.jar;%APP_HOME%\lib\maven-model-3.0.4.jar;%APP_HOME%\lib\maven-model-builder-3.0.4.jar;%APP_HOME%\lib\maven-repository-metadata-3.0.4.jar;%APP_HOME%\lib\plexus-component-annotations-1.5.5.jar;%APP_HOME%\lib\wagon-http-shared4-2.2.jar;%APP_HOME%\lib\httpclient-4.1.2.jar;%APP_HOME%\lib\httpcore-4.1.2.jar;%APP_HOME%\lib\sisu-inject-bean-2.2.3.jar;%APP_HOME%\lib\plexus-interpolation-1.14.jar;%APP_HOME%\lib\jsoup-1.6.1.jar;%APP_HOME%\lib\commons-logging-1.1.1.jar;%APP_HOME%\lib\commons-io-2.0.1.jar;%APP_HOME%\lib\commons-codec-1.4.jar;%APP_HOME%\lib\sisu-guice-3.0.3-no_aop.jar;%APP_HOME%\lib\cglib-2.2.2.jar;%APP_HOME%\lib\asm-3.3.1.jar;%APP_HOME%\lib\plexus-utils-3.0.jar

@rem Execute clojure
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %CLOJURE_OPTS%  -classpath "%CLASSPATH%" com.twosigma.beakerx.clojure.kernel.Clojure %CMD_LINE_ARGS%

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable CLOJURE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%CLOJURE_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
