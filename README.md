# Synco

Syncs files between my server and local machine only sending the diff.



### Building Server

Building 

```
docker build -t syncoserver .
```

Running 
```
docker run -p 8000:8000  -v ~/synco:/app/data syncoserver
```

Running the tests

```
./tests.sh
```



