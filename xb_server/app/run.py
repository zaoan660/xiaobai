import os
import sys

import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def main():
    if len(sys.argv) == 3:
        uvicorn.run(
            "app.app:app",
            host=sys.argv[1],
            port=int(sys.argv[2]),
            reload=True,
        )
    else:
        uvicorn.run("app.app:app", host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
    main()