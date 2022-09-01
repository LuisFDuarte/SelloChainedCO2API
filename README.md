# SelloChainedCO2API

API que consulta datos de  API CO2 signal  https://www.co2signal.com/ y devuelve archivos JSON con metadata para NFTs dinamicos.

# Instrucciones despliegue en Heroku
Se depliega aplicación como contenedor de docker
https://api-co2.herokuapp.com/docs

- heroku login
- heroku container:login
- heroku create api-co2
- heroku git:remote -a  api-co2
- heroku container:push web --app api-co2
- heroku container:release web --app api-co2
