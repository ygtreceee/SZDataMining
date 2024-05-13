<script setup>
import { ref, onBeforeMount, onMounted } from "vue";
import { getDayInformation } from "../api/getDayInformation";

const content = ref("");
let title = ref(""); // 标题
let firstSaleDay = ref(""); // 当日一手房成交
let firstSaleMonth = ref(""); // 当日一手房累计成交
let secondSaleDay = ref(""); // 当日二手房成交
let secondSaleMonth = ref(""); // 当月二手房累计成交

let transactionRatio = ref(""); // 二手房近三月成交环比 
let numberTransactSecondhandHousePastFourWeek = ref([]) // 二手房近四周成交套数
let numberSecondhandHouseSoldRecentThreeMonth = ref([]) //二手房近三月成交套数 

const props = defineProps({
  weekday: Number,
});

const curWeekday = ref(); // 存储今天是星期几


onBeforeMount(async () => {
  // 数据初始化
  content.value = await getDayInformation(props.weekday);
  console.log(content.value)
  firstSaleDay.value = content.value.yesterdayYsf;
  firstSaleMonth.value = content.value.lastMonthYsf;
  secondSaleDay.value = content.value.yesterdayEsf;
  secondSaleMonth.value = content.value.lastMonthEsf;

  transactionRatio.value = content.value.transactionRatio;
  numberTransactSecondhandHousePastFourWeek.value = content.value.numberTransactSecondhandHousePastFourWeek
  numberSecondhandHouseSoldRecentThreeMonth.value = content.value.numberSecondhandHouseSoldRecentThreeMonth

  console.log(numberTransactSecondhandHousePastFourWeek.value)
  const today = new Date();
  curWeekday.value = today.getDay();

  title.value = content.value.title;
});
</script>

<template>
  <h2>{{ title }} 深圳成交简报</h2>
  <hr />
  <div class="container">
    <div class="dailyContent">
      <div class="fontBold">
        当日一手房成交: <span class="fontBig">{{ firstSaleDay }}套</span>
      </div>
      <div class="fontBold">
        当月一手房累计成交: <span class="fontBig">{{ firstSaleMonth }}套</span>
      </div>
      <div class="ColorRed fontBold">
        当日二手房成交: <span class="fontBig">{{ secondSaleDay }}套</span>
      </div>
      <div class="ColorRed fontBold">
        当月二手房累计成交:
        <span class="fontBig">{{ secondSaleMonth }}套</span>
      </div>
    </div>
    <div class="compareContent">
      <div class="mouth" v-if="numberTransactSecondhandHousePastFourWeek != null && numberTransactSecondhandHousePastFourWeek.length != null">
        <div class="fontBold">二手房近四周成交套数</div>
        <table>
          <thead>
            <tr>
              <th v-for="(value, index) in numberTransactSecondhandHousePastFourWeek[0]" :key="index">
                {{ value }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                v-for="(value, index) in numberTransactSecondhandHousePastFourWeek[1]"
                :key="index"
              >
                {{ value }} 套
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mouth" v-if="numberSecondhandHouseSoldRecentThreeMonth != null && numberSecondhandHouseSoldRecentThreeMonth.length != null">
        <div class="fontBold">二手房近三月成交套数</div>
        <table>
          <thead>
            <tr>
              <th v-for="(value, index) in numberSecondhandHouseSoldRecentThreeMonth[0]" :key="index">
                {{ value }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                v-for="(value, index) in numberSecondhandHouseSoldRecentThreeMonth[1]"
                :key="index"
              >
                {{ value }} 套
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mouth">
        <div class="fontBold">二手房近三月成交环比</div>
        <table>
          <thead>
            <tr>
              <th v-for="(value, index) in transactionRatio[0]" :key="index">
                {{ value }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                v-for="(value, index) in transactionRatio[1]"
                :key="index"
                :class="{ 'bold-text': index === 0 }"
              >
                {{ value }}{{ index === 0 ? "" : "%" }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="remark">
      <p>备注：</p>
      <p>数据来源：深圳市房地产信息平台</p>
      <p>一手房成交数据为网签口径</p>
      <p>二手房成交数据为过户口径</p>
      <div class="line">
        <div class="footer">&nbsp&nbsp总要有底线吧&nbsp&nbsp</div>
      </div>
      <div class="publicAccount">
        <img src="../assets/TwoDimensionalCode.jpg" alt="二维码图片" />
        <div class="context">
          <p>扫描二维码，关注深房先知!</p>
          <p>每日 9: 30 分 自动推送深圳成交信息</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 加粗字体类 */

.fontBold {
  font-weight: bold;
}
.fontBig {
  font-size: 5vmin;
  font-weight: bold;
}

/* 红色类 */
.ColorRed {
  color: #c92a2a;
}

/* 大容器 */
.container {
  font-size: 4vmin;
  display: flex;
  flex-direction: column;
  gap: 7vh;
}

/* 第一部分样式 */
.dailyContent,
.areaContent {
  display: flex;
  flex-direction: column;
  gap: 1.5vh;
}

/* 第二部分样式 */
.compareContent {
  display: flex;
  flex-direction: column;
  gap: 4vh;
}

/* 图表样式 */
.chart {
  height: 50vw;
  width: 100vw;
}

/* 备注样式 */
.remark {
  font-size: 1vmin;
}

.line {
  position: relative;
  margin: 0 auto;
  background-color: #eeeeee;
  height: 0.2vh;
  width: 100vw;
  margin-bottom: 1vh;
}

.footer {
  background-color: white;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5vmin;
}

hr {
  border-top: 1px solid #eeeeee;
}

/* 表格相关 */
table {
  table-layout: fixed;
  width: 90vw;
  margin-top: 1vh;
  border-collapse: collapse;
  font-size: 2vmin;
}

th,
td {
  border: 1px solid #999;
  text-align: center;
  padding: 2vw 0;
}

.bold-text {
  font-weight: bold;
}

/* 底部二维码 */

img {
  width: 20vw;
  height: 20vw;
}

.publicAccount {
  display: flex;
  font-size: 3.5vmin;
  gap: 8vw;
  align-items: center;
}
</style>
