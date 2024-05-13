const express = require("express");
const morgan = require("morgan");
const cors = require("cors");
const dotenv = require("dotenv");
const bodyParser = require("body-parser");

dotenv.config({ path: "./config.env" });

const mongoose = require("mongoose");

// 数据库连接
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

mongoose
  .connect(process.env.DATABASE_LOCAL, {
    useNewUrlParser: true,
    useCreateIndex: true,
    useFindAndModify: false,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("DB connection successful");
  })
  .catch((error) => {
    console.error("DB connection error:", error);
  });

// 设置跨域
app.use(cors());

if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

app.use(express.json());

// 接收的数据模型
const informationSchema = new mongoose.Schema({
  weekday: {
    type: Number,
    require: [true, "需要传递该信息是周几的"],
  },
  content: {
    type: mongoose.Schema.Types.Mixed,
    require: [true, "需要传递当前信息内容"],
  },
});
const Information = mongoose.model("WeekDayInformation", informationSchema);

/**
 * 接收 python 发送的信息
 */
app.post("/api/v1/information", async (req, res) => {
  const { weekday, content } = req.body;

  // 查找对应 weekday 的消息
  let information = await Information.findOne({ weekday });

  if (information) {
    information = await Information.findByIdAndUpdate(
      { _id: information._id },
      { content }
    );
  } else {
    information = await Information.create({ weekday, content });
  }

  res.status(200).json({
    status: "success",
    message: "消息保存成功",
    data: {
      information,
    },
  });
});

/**
 * 网站通过该接口拉取数据
 */
app.get("/api/v1/information/:weekday", async (req, res) => {
  console.log(req.params);
  const { weekday } = req.params;
  try {
    let information = await Information.findOne({ weekday });

    if (information) {
      res.status(200).json({
        status: "success",
        message: "当天信息报告获取成功",
        data: {
          information,
        },
      });
    } else {
      res.status(200).json({
        status: "fail",
        message: "未查找到当前的信息报告",
      });
    }

    res.status(200).json({
      status: "success",
    });
  } catch (err) {
    console.log(err);
  }
});

const port = 3000;
app.listen(port, () => {
  console.log(`APP running on port ${port}...`);
});
