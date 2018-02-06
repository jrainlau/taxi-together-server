const Router = require('koa-router')
const ImageController = require('../controller/image.js')
const multer = require('koa-multer')
const path = require('path')

const img = new Router()
const storage = multer.diskStorage({
  destination: path.join(__dirname, '../static/images'),
  filename (req, file, cb) {
    cb(null, file.originalname)
  }
})
const upload = multer({ storage })

img
  .post('/upload', upload.single('img'), ImageController.upload)

module.exports = img
