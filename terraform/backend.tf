terraform {
  backend "s3" {
    bucket         = "weather-app-tf-state-bucket"
    key            = "eks/terraform.tfstate"
    region         = "ap-south-1"
    
  }
}
