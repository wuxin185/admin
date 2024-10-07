import axios from "axios";

let baseUrl = "http://localhost:8000/";

const httpService = axios.create({
  baseURl: baseUrl,
  timeout: 3000,
});

httpService.interceptors.request.use(
  function (config) {
    config.headers.AUTHORIZATION = window.sessionStorage.getItem("token");
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

httpService.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export function get(url, params = {}) {
  return new Promise((resolve, reject) => {
    httpService({
      url: baseUrl + url,
      method: "get",
      params: params,
    })
      .then((response) => {
        console.log(response);

        resolve(response);
      })
      .catch((error) => {
        console.log(error);

        reject(error);
      });
  });
}

export function post(url, params = {}) {
  return new Promise((resolve, reject) => {
    httpService({
      url: baseUrl + url,
      method: "post",
      params: params,
    })
      .then((response) => {
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function del(url, params = {}) {
  return new Promise((resolve, reject) => {
    httpService({
      url: baseUrl + url,
      method: "delete",
      params: params,
    })
      .then((response) => {
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function fileUpload(url, params = {}) {
  return new Promise((resolve, reject) => {
    httpService({
      url: baseUrl + url,
      method: "post",
      data: params,
      headers: { "Content-Type": "multipart/form-data" },
    })
      .then((response) => {
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function getServerUrl() {
  return baseUrl;
}

export default {
  get,
  post,
  del,
  fileUpload,
  getServerUrl,
};
