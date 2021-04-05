(function (factory) {
  typeof define === 'function' && define.amd ? define('index', factory) :
  factory();
}((function () { 'use strict';

  window.onload = () => {
    console.log('Hi');
    const app = Vue.createApp({
      data() {
        return {
          rows: [],
          cols: [],
          modelCols: [],
          modelRows: [],
          returnCols: [],
          returnRows: [],
          month: undefined,
          year: undefined,
          slide_05_heading: undefined,
          slide_06_heading: undefined
        };
      },

      async mounted() {
        await d3.csv("stats.csv", data => {
          if (typeof data === 'object') {
            this.rows.push(data);
          }
        });
        this.cols = Object.keys(this.rows[0]);
        await d3.csv("modelStats.csv", data => {
          if (typeof data === 'object') {
            this.modelRows.push(data);
          }
        });
        this.modelCols = Object.keys(this.modelRows[0]);
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const d = new Date();
        this.month = monthNames[d.getMonth()];
        this.year = new Date().getFullYear();
        await d3.csv("returnStats.csv", data => {
          if (typeof data === 'object') {
            this.returnRows.push(data);
          }
        });
        this.returnCols = Object.keys(this.returnRows[0]);
        this.returnRows.forEach((rCol, index) => {
          for (let [key, value] of Object.entries(rCol)) {
            // console.log(value);
            if (value) {
              // value = value * 100;
              const t = this.returnRows[index];
              console.log(parseFloat(value));

              if (parseFloat(value) > 10) ; else {
                t[key] = (parseFloat(value) * 100).toFixed(1) + '%';
              }
            }
          }
        }); // Load Headings

        const httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', 'slide1.txt', true);

        httpRequest.onreadystatechange = () => {
          // Process the server response here.
          if (httpRequest.status === 200) {
            // Perfect!
            console.log(httpRequest.response);
            this.slide_05_heading = httpRequest.response.replace('"', '').replace('"', '');
          }
        };

        httpRequest.send();
        const httpRequest2 = new XMLHttpRequest();
        httpRequest2.open('GET', 'slide2.txt', true);

        httpRequest2.onreadystatechange = () => {
          // Process the server response here.
          if (httpRequest2.status === 200) {
            // Perfect!
            console.log(httpRequest2.response);
            this.slide_06_heading = httpRequest2.response.replace('"', '').replace('"', '');
            this.slide_06_heading = this.slide_06_heading.split('|');
          }
        };

        httpRequest2.send();
      },

      methods: {}
    });
    app.mount('#app');
  };

})));
