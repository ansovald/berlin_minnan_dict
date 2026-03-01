# Berlin Minnan Dictionary

This is the code for a dictionary for Hokkien Chinese that combines publicly available data from Wiktionary with the [MoE-Dictionary](https://sutian.moe.edu.tw/). 

It is currently hosted by Humboldt University of Berlin: [Berlin Minnan Dictionary](https://minnan-iaaw.hu-berlin.de/?hanzi=%E6%AD%A1%E8%BF%8E).


### Building and Running

Using Docker Compose (recommended):
```bash
docker-compose up -d
```

Or using Docker directly:
```bash
docker build -t berlin-minnan-dict .
docker run -p 80:80 -v $(pwd)/dictionary-backend/data:/app/backend/data berlin-minnan-dict
```

The application will be available at http://localhost

### Development

For local development, I recommend using:

> docker-compose down && docker-compose build && docker-compose up -d