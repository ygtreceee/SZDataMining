import axios from "axios";
export const getDayInformation = (weekday) => {
  return new Promise((resolve, reject) => {
    axios({
      url: `http://114.132.235.86:3000/api/v1/information/${weekday}`,
      method: "GET",
    }).then((result) => {
      const data = result.data.data.information.content;
      resolve(data);
    });
  });
};
