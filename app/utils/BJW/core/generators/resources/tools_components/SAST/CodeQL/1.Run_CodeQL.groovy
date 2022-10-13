stage('Run CodeQL') {
    sh "/home/onedayginger/bibim-bob/bob-codeql/run.py -l javascript -s ${env.WORKSPACE} -o /home/onedayginger"
}