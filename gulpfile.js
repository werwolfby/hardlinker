var path = require('path');
var del = require('del');

var gulp = require('gulp');
var gutil = require("gulp-util");
var zip = require('gulp-zip');
var webpack = require('webpack');

var pkg = require('./package.json');

var paths = {
  index_pages: ['./src/*.html'],
  dest: 'webapp',
  release: 'dist'
};

gulp.task('default', ['clean', 'webpack']);

gulp.task('clean', function () {
  return del.sync([paths.dest]);
});

function callWebpack(callback, config) {
  webpack(config, function (err, stats) {
    if(err) throw new gutil.PluginError("webpack", err);
    gutil.log("[webpack]", stats.toString());
    callback();
  });
}

gulp.task('webpack', function (callback) {
  callWebpack(callback, require('./webpack.config'));
});

gulp.task('webpack-production', function (callback) {
  callWebpack(callback, require('./webpack.production.config'));
});

gulp.task('clean-release', function () {
  return del.sync([paths.release]);
});

gulp.task('release', ['dist'], function () {
  return gulp.src([paths.release + '/**/*.*'])
    .pipe(zip(pkg.name + '-' + pkg.version + '.zip'))
    .pipe(gulp.dest('.'));
});

gulp.task('dist', ['clean-release', 'copy-python', 'copy-webapp', 'copy-desc']);

gulp.task('copy-python', function () {
  return gulp.src(['./**/*.py', '!./tests*/**/*.*', '!./' + paths.release + '/**/*.py'])
    .pipe(gulp.dest(paths.release));
});

gulp.task('copy-webapp', ['webpack-production'], function () {
  return gulp.src([path.join(paths.dest, '**/*.*'), '!./**/*.map'])
    .pipe(gulp.dest(path.join(paths.release, paths.dest)));
});

gulp.task('copy-desc', function () {
  return gulp.src(['./package.json', './requirements.txt'])
    .pipe(gulp.dest(paths.release));
})
