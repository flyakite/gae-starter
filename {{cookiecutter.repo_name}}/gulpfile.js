var gulp = require('gulp'),
	sass = require('gulp-sass'),
	minifycss = require('gulp-minify-css'),
	notify = require('gulp-notify'),
	uglify = require('gulp-uglify'),
	rename = require('gulp-rename'),
	livereload = require('gulp-livereload'),
	connect = require('gulp-connect');
	
var config = {
	assetsDir: './assets/',
	bowerDir: './bower_components/',
	templatesDir: './app/templates/',
	staticDir: './app/static/'
};


//run livereload
gulp.task('connect', function() {
	connect.server({
		root: 'app',
		livereload: true
	});
});

//font awesome
gulp.task('fontawesome', function() {
	return gulp
		.src(config.bowerDir + 'fontawesome/fonts/**.*')
		.pipe(gulp.dest(config.staticDir + 'fonts'));
});

//styles
//bootstrap are not included, use @import in sass to import needed styles
//see bootstrap-sass-official
gulp.task('styles', function() {
	return gulp
		.src([
			config.assetsDir + 'sass/**/*.sass',
			config.bowerDir + 'fontawesome/scss/**/*.scss'
		])
		.pipe(sass({
			outputStyle: 'compressed'
			})
			.on('error', notify.onError(function(error) {
				return "Error:" + error.message;
			}))
		)
		.pipe(gulp.dest(config.staticDir + 'css'))
		.pipe(rename({suffix: '.min'}))
		.pipe(minifycss())
		.pipe(gulp.dest(config.staticDir + 'css'))
		.pipe(connect.reload());
});

//html
gulp.task('html', function() {
	gulp.src(config.templatesDir + '**/*.html')
		.pipe(connect.reload());
});


gulp.task('uglifyjs', function() {
  return gulp.src(config.assetsDir + 'js/**/*.js')
    .pipe(uglify())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest(config.staticDir + 'js/'))
		.pipe(connect.reload());
});

gulp.task('copy', function() {
	//copy static assets to static folder
	gulp.src(config.assetsDir + '*.*')
		.pipe(gulp.dest(config.staticDir))

	//copy static images to static folder
	gulp.src(config.assetsDir + 'img/**/*')
		.pipe(gulp.dest(config.staticDir + 'img'))

	//copy js in bower to static folder
	gulp.src([
		config.bowerDir + 'modernizr-min/modernizr.min.js',
		config.bowerDir + 'bootstrap-sass-official/assets/javascripts/bootstrap.min.js',
		config.bowerDir + 'jquery/dist/jquery.min.js'
		])
		.pipe(gulp.dest(config.staticDir + 'js/'))
		.pipe(connect.reload());
});

gulp.task('watch', function() {
	gulp.watch(config.templatesDir + '**/*.html', ['html']);
	gulp.watch(config.assetsDir + 'sass/**/*.sass', ['styles']);
	gulp.watch(config.assetsDir + 'js/**/*.js', ['uglifyjs']);
	gulp.watch(config.assetsDir + '**/*', ['copy']);
});


gulp.task('default', ['connect', 'fontawesome', 'copy', 'styles', 'uglifyjs', 'watch'])

