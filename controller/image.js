class ImageController {
  async upload (ctx) {
    try {
      if (ctx.req.file) {
        ctx.req.file.path = ctx.req.file.path.split('static')[1]
        console.log('上传成功')
        ctx.body = img
      }
    } catch (err) {
      ctx.throw(422)
    }
  }
}

module.exports = new ImageController()
