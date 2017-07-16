/*global module:false*/
/* jshint node: true */
module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        // Task configuration.
        pkg: grunt.file.readJSON('package.json'),
        jshint_reporter: require('jshint-stylish'),
        jshint: {
            options: {
                curly: true,
                eqeqeq: true,
                immed: true,
                latedef: true,
                newcap: true,
                noarg: true,
                sub: true,
                undef: true,
                unused: true,
                boss: true,
                eqnull: true,
                browser: true,
                globals: {
                    jQuery: true
                },
                reporter: require('jshint-stylish') // use jshint-stylish to make our errors look and read good
            },
            gruntfile: {
                src: 'Gruntfile.js'
            },
            build: {
                src: ['static/javascript/*.js'],
                options : {
                    jshintrc : '.jshintrc'
                }
            }
        },
		browserify: {
            build: {
                files: {
                    // destination for transpiled js : source js
                    'src/babel/ltt.js': 'src/js/ltt.js'
                },
                options: {
                    transform: [['babelify', { presets: "es2015" }]],
                    browserifyOptions: {
                        debug: true
                    }
                }
            }
        },
        uglify: {
            options: {
                banner: '/*\n <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> \n*/\n'
            },
            build: {
                files: {
                    'static/javascript/ltt.js': ['src/babel/ltt.js']
                }
            }
        },
        cssmin: {
            build: {
                files: {
                    'static/css/ltt.css': [
                        'src/css/base_style.css',
                        'src/css/genre.css',
                        'src/css/ltt_style.css',
                        'src/css/style.css'
                    ],
                    'static/css/index.css': [
                        'src/css/base_style.css',
                        'src/css/index_style.css',
                        'src/css/style.css'
                    ],

                }
            }
        },
        watch: {
            gruntfile: {
                files: '<%= jshint.gruntfile.src %>',
                tasks: ['jshint:gruntfile']
            },
            all: {
                files: '<%= jshint.all.src %>',
                tasks: ['jshint:all']
            }
        }
    });

    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('jshint-stylish');
    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Default task.
    grunt.registerTask('default', ['jshint', 'browserify', 'uglify', 'cssmin']);


};
