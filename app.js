const express = require('express');
const multer = require("multer");
const {spawn} = require('child_process');
const path = require('path');
const app = express();
const port = 3000;
const bodyParser = require('body-parser');
const morgan = require('morgan');
const jwt = require('jsonwebtoken');
const config = require('./configurations/config');

const puppeteer = require('puppeteer');
const fs = require('fs');

app.use(express.static(__dirname));

//set secret
app.set('Secret', config.secret);

// use morgan to log requests to the console
app.use(morgan('dev'));

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// parse application/json
app.use(bodyParser.json());

// 
// AUTH (JWT TOKEN)
// 
app.post('/authenticate', (req,res) => {
  
  if(req.body.username === 'Arquant'){

    if(req.body.password === '9dRgUpCE'){
      //if eveything is okey let's create our token 

    const payload = { check:  true };

      var token = jwt.sign(payload, app.get('Secret'), {
        expiresIn: 1440 // expires in 24 hours
      });

      res.json({
        message: 'done',
        token: token
      });

    }else{
      res.json({message: 'please check your password !'});
    }

  }else{

    res.json({message: '404'});

  }

});
// 
// ./AUTH (JWT TOKEN)
// 

// 
//
//

var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, 'Presentation_2021-2');
  },
  filename: function (req, file, callback) {
    callback(null, file.originalname);
  }
});

var upload = multer({ storage : storage });

//   
// 
// 

const  ProtectedRoutes = express.Router(); 

app.use('/api', ProtectedRoutes);

ProtectedRoutes.use((req, res, next) =>{


  // check header for the token
  var token = req.headers['access-token'];

  // decode token
  if (token) {

    // verifies secret and checks if the token is expired
    jwt.verify(token, app.get('Secret'), (err, decoded) =>{      
      if (err) {
        return res.json({ message: 'invalid token' });    
      } else {
        // if everything is good, save to request for use in other routes
        req.decoded = decoded;    
        next();
      }
    });

  } else {
    // if there is no token  
    res.send({ 
        message: 'No token provided.'
    });

  }
});
ProtectedRoutes.get('/getAllProducts',(req,res)=>{
  let products = [
      {
          id: 1,
          name:"cheese"
      },
      {
         id: 2,
         name:"carottes"
     }
  ]
 
  res.json(products)
 
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/generate.html'));
});

ProtectedRoutes.get('/generate', (req, res) => {
 
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('py', ['ARQUANT_slides_for_Arseny.py']);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend)
    });

    setTimeout(() => {
        python.kill('SIGINT');

        (async () => {
          // launch a new chrome instance
          const browser = await puppeteer.launch({
            headless: true
          })
        
          // create a new page
          const page = await browser.newPage()
        
          // await page.goto('http://35.176.63.20:3000/presentation.html', {waitUntil: 'networkidle0'});
          await page.goto('http://localhost:3000/presentation.html', {waitUntil: 'networkidle0'});
        
          page.addStyleTag(
            {'content': '@page { size: A4 landscape; }'}
          )
          // set your html as the pages content
        //   const html = fs.readFileSync(`${__dirname}/dist/index.html`, 'utf8')
        //   await page.setContent(html, {
        //     waitUntil: 'networkidle0'
        //   })
        
          // create a pdf buffer
          const pdfBuffer = await page.pdf({
            format: 'A4',
            landscape: true
          })
        
          // or a .pdf file
          await page.pdf({
            format: 'A4',
            path: `${__dirname}/ARQuant_Presentation.pdf`
          })
        
          // close the browser
          await browser.close()

          console.log('Presentatin Generated');
        })()

    }, 10000);
 
});

ProtectedRoutes.post("/upload", upload.array('filedata', 4), (req, res, next) => {
    const files = req.files
    if (!files) {
      const error = new Error('Please choose files')
      error.httpStatusCode = 400
      return next(error)
    }
   
      res.send(files)
    
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`))