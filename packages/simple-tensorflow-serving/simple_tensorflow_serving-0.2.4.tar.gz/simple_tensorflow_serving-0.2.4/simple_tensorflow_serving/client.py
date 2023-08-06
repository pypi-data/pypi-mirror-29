#!/usr/bin/env python

import requests

def main():
  endpoint = "http://127.0.0.1:8500"
  json_data = {"data": {"input": [[1, 1], [1, 1]]} }
  result = requests.post(endpoint, json=json_data)
  print(result.text)

if __name__ == "__main__":
  main()
  