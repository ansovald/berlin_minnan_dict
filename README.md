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

For local development, you can still run the frontend and backend separately:

**Backend:**
```bash
cd dictionary-backend
pip install -r requirements.txt
python dictionary_backend.py
```

**Frontend:**
```bash
cd dictionary-frontend
npm install
REACT_APP_API_URL=http://localhost:5000/api npm start
``` 