# PPE HK

## How to run

1. Create virtual environment.

```
virtualenv .venv
```

2. Activate virtual environment.

```
source .venv/bin/activate
```

3. Change to app directory.

```
cd app
```

4. Run the app.

```
uvicorn app:app --host 0.0.0.0 --port 9095
```
