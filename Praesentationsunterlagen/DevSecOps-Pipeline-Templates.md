# DevSecOps Pipeline-Templates - Externe Repository-Informationen

Dieses Dokument enthält Links und Informationen zum DevSecOps Pipeline-Template, das über den QR-Code in der Präsentation zugänglich ist.

## Repository-Link

GitHub Repository: https://github.com/AndroMars/devsecops

## Enthaltene Templates

Das Repository enthält vollständige CI/CD-Pipeline-Konfigurationen mit integrierten Sicherheitsmaßnahmen für verschiedene Plattformen:

### GitLab CI/CD

```yaml
stages:
  - build
  - security
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  SECURE_LOG_LEVEL: info

build:
  stage: build
  script:
    - echo "Building application..."
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG .

sast:
  stage: security
  script:
    - echo "Running SAST scan..."
    - semgrep --config=p/owasp-top-ten --output sast-results.json .
  artifacts:
    paths:
      - sast-results.json

dependency_check:
  stage: security
  script:
    - echo "Checking dependencies..."
    - owasp-dependency-check --project "My Project" --out dep-check-report.html --scan .
  artifacts:
    paths:
      - dep-check-report.html

container_scan:
  stage: security
  script:
    - echo "Scanning container image..."
    - trivy image --format json --output trivy-results.json $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
  artifacts:
    paths:
      - trivy-results.json

test:
  stage: test
  script:
    - echo "Running tests..."
    - npm test

deploy:
  stage: deploy
  script:
    - echo "Deploying application..."
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
  only:
    - main
```

### GitHub Actions

```yaml
name: DevSecOps Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build
      run: |
        echo "Building application..."
        docker build -t myapp:${{ github.sha }} .

  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: SAST scan
      uses: returntocorp/semgrep-action@v1
      with:
        config: p/owasp-top-ten
    
    - name: Dependency check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'My Project'
        path: '.'
        format: 'HTML'
    
    - name: Container scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'myapp:${{ github.sha }}'
        format: 'json'
        output: 'trivy-results.json'
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          dependency-check-report.html
          trivy-results.json

  test:
    needs: security
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy
      run: echo "Deploying application..."
```

### Azure DevOps

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Building application..."
    - task: Docker@2
      inputs:
        command: build
        dockerfile: 'Dockerfile'
        tags: '$(Build.BuildId)'

- stage: Security
  jobs:
  - job: SecurityJob
    steps:
    - script: |
        echo "Running SAST scan..."
        npm install -g semgrep
        semgrep --config=p/owasp-top-ten --output sast-results.json .
      displayName: 'SAST Scan'
    
    - script: |
        echo "Checking dependencies..."
        npm install -g @owasp/dependency-check
        dependency-check --project "My Project" --out dep-check-report.html --scan .
      displayName: 'Dependency Check'
    
    - script: |
        echo "Scanning container image..."
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image myapp:$(Build.BuildId)
      displayName: 'Container Scan'

- stage: Test
  jobs:
  - job: TestJob
    steps:
    - script: npm test
      displayName: 'Run Tests'

- stage: Deploy
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - job: DeployJob
    steps:
    - script: echo "Deploying application..."
      displayName: 'Deploy'
```

## Security Tools Integration

Das Repository enthält auch Anleitungen zur Integration folgender Sicherheitstools:

1. **SAST-Tools**:
   - SonarQube
   - Semgrep
   - Checkmarx

2. **SCA-Tools**:
   - OWASP Dependency-Check
   - Snyk
   - Dependabot

3. **Container-Security**:
   - Trivy
   - Clair
   - Anchore

4. **Infrastructure as Code Scanner**:
   - TFSec
   - Checkov
   - CloudSploit

## Best Practices

Das Repository enthält auch Dokumentation zu DevSecOps Best Practices:

- Policy as Code
- Secrets Management
- Compliance as Code
- Security Testing Automation
- Incident Response Automation
