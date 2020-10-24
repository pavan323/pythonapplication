node {
    def app

    stage('Clone repository') {
        /* Cloning the Repository to our Workspace */

        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image */

        /*app = docker.build("manoj96/app")*/
	  sh "docker build -t manoj96/app:${currentBuild.number} ."
    }

    stage('Push image') {
        /* 
			You would need to first register with DockerHub before you can push images to your account
		
        docker.withRegistry('https://registry.hub.docker.com', 'Docker') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
            } */
	    withCredentials([string(credentialsId: 'DockerUsername', variable: 'DockerUsername'), string(credentialsId: 'DockerPassword', variable: 'DockerPassword')]) {
		    sh "docker login -u ${DockerUsername} -p ${DockerPassword}"
		    
             }
	    sh "docker push manoj96/app:${currentBuild.number}"
                echo "Trying to Push Docker Build to DockerHub"
    }
}
