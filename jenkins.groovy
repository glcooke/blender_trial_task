pipeline {
    agent {
        label 'Blender Node'
    }
    stages {
        stage('Dir cleaning') {
            steps {
                script {
                    def output_path = params.output_path
                }
                dir (output_path) {
                    deleteDir()
                }
            }
        }
        stage('Checkout from GitHub') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/glcooke/blender_trial_task']]])
                }
            }
        }
        stage('Run Scripts') {
            steps {
                script {
                    def blender_path = params.blender_path
                    def x_resolution = params.x_resolution
                    def y_resolution = params.y_resolution
                }
                withPythonEnv('D:\\jenkins\\Blender Node\\workspace\\Python310\\python.exe') {
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