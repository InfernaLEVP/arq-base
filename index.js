(function (factory) {
  typeof define === 'function' && define.amd ? define('index', factory) :
  factory();
}((function () { 'use strict';

  window.onload = () => {
    
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
          slide_06_heading: undefined,
          pDate: undefined
        };
      },

      async mounted() {
        await d3.csv("Presentation_2021-2/Stats_for_print.csv", data => {
          if (typeof data === 'object') {
            this.rows.push(data);
          }
        });
        this.cols = Object.keys(this.rows[0]);
        
        await d3.csv("Presentation_2021-2/FF.csv", data => {
          if (typeof data === 'object') {
            this.modelRows.push(data);
          }
        });
        this.modelCols = Object.keys(this.modelRows[0]);
        
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const d = new Date();
        this.month = monthNames[d.getMonth()];
        this.year = new Date().getFullYear();
        await d3.csv("Presentation_2021-2/Fact_Sheet_after_fees.csv", data => {
          if (typeof data === 'object') {
            this.returnRows.push(data);
          }
        });
        this.returnCols = Object.keys(this.returnRows[0]);
        this.returnRows.forEach((rCol, index) => {
          for (let [key, value] of Object.entries(rCol)) {
            
            if (value) {
              // value = value * 100;
              const t = this.returnRows[index];
              

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

        // const httpRequest3 = new XMLHttpRequest();
        // httpRequest3.open('GET', 'pFF.json', true);

        // httpRequest3.onreadystatechange = () => {
        //   // Process the server response here.
        //   if (httpRequest3.status === 200) {

        //     console.warn(httpRequest3.response);
        //     const data = JSON.parse(httpRequest3.response);
        //     // console.log(data);

        //     this.modelRows.push(data);
        //     this.modelCols = Object.keys(this.modelRows[0]);
        //   }
        // };

        // fetch('/pFF.json')
        //   .then(response => response.json())
        //   .then(data => {

            
        //     const modelTableData = JSON.parse(data);
        //     const modelTableDataParsed = Object.entries(res);

        //     for(let i = 0; i < modelTableDataParsed.length; i++){
        //       const colName = modelTableDataParsed[i];
        //       this.modelCols.push(colName[0]);
        //     }
        //     console.log(Object.entries(res));
            
        //     this.modelCols = Object.keys(this.modelRows[0]);
        //   });

        // httpRequest3.send();

      },

      methods: {}
    });
    app.mount('#app');
  };

})));
