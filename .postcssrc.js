const plugins = [
  require('autoprefixer')
]

if (process.env.QUASAR_RTL) {
  plugins.push(
    require('postcss-rtl')({}) // eslint-disable-line @typescript-eslint/no-var-requires
  )
}

module.exports = {
  plugins
}
