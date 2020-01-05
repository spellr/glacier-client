docker build --tag glacier_client .

for /f %%i in ('docker create glacier_client') do set ID=%%i

docker cp %ID%:/glacier/target/GlacierClient.deb .

docker rm -v %ID%