const Koa = require('koa')
const path = require('path')
const router = require('./router/index.js')
const bodyParser = require('koa-bodyparser')
const static = require('koa-static')
const views = require('koa-views')
const cors = require('koa2-cors')

const app = new Koa()

app
  .use(cors({ origin: '*' }))
  .use(views(path.join(__dirname, './views'), { extension: 'ejs' }))
  .use(bodyParser())
  .use(router.routes())
  .use(router.allowedMethods())
  .use(static(path.join(__dirname, './static')))

app.listen(3000, () => {
  console.log('Listening at port 3000');
})
