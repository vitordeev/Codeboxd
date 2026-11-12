export default {
  multipass: true,
  plugins: [{name: 'preset-default', params: {overrides: {
    cleanupIds: false, collapseGroups: false, mergePaths: false,
    removeUnknownsAndDefaults: false, removeUselessStrokeAndFill: false
  }}}]
};
