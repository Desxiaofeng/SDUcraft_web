if exist "D:\web\nginx-1.24.0\logs\nginx.pid" (
	nginx.exe -s reload
) else (
	nginx.exe
)

