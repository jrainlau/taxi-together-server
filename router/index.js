const Router = require('koa-router')

const router = new Router()

;[
  'bill'
].forEach((route) => {
  const routeInstance = require(`./${route}.js`)
  router.use(`/taxi/${route}`, routeInstance.routes(), routeInstance.allowedMethods())
})

module.exports = router
