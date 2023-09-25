pipeline {
    agent any
    stages {
        stage('Dir cleaning') {
            steps {
                dir ('D:\\test_results') {
                    deleteDir()
                }
            }
        }
        stage('Checkout from GitHub') {
            steps {
                script {
                    // Checkout the GitHub repository
                    checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/glcooke/blender_trial_task']]])
                }
            }
        }
        stage('Run Scripts') {
            steps {
                script {
                    // Access the parameter value
                    def blender_path = params.blender_path
                    def output_path = params.output_path
                    def x_resolution = params.x_resolution
                    def y_resolution = params.y_resolution
                }
                withPythonEnv('D:\\jenkins\\Blender Node\\workspace\\Python310\\python.exe') {
                    // Execute your scripts here
                    bat '''
                        pip install -r requirements.txt
                        python main.py %blender_path% %output_path% %x_resolution% %y_resolution%
                    '''

                }
            }
        }
        stage('Archive') {
            steps {
                dir('D:\\test_results') {
                    archiveArtifacts artifacts: '**', allowEmptyArchive: true
                }
            }
        }
    }
}