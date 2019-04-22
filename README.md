# revolut_assignment
Revolut Assignment for Data Engineerning


Build Docker Image 
```
docker build -t revolut_assignment .
```

Run Docker Container
```
docker run --name revolut_api -d -p 8000:5000 revolut_assignment:latest
```

Login to Docker Container
```
docker exec -it revolut_api /bin/bash
```