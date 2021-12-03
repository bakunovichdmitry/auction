terraform {
  required_providers {
    heroku = {
      source = "heroku/heroku"
      version = "3.2.0"
    }
  }
}

terraform {
  backend "remote" {
    organization = "itechart-auction"

    workspaces {
      name = "gh-actions-auction"
    }
  }
}

provider "heroku" {
}

resource "heroku_app" "itechart-auction" {
  name = "itechart-auction-2"
  region = "us"
  stack = "container"
}


resource "heroku_addon" "postgres" {
  app = heroku_app.itechart-auction.id
  plan = "heroku-postgresql:hobby-dev"
}

resource "heroku_addon" "redis" {
  app = heroku_app.itechart-auction.id
  plan = "heroku-redis:hobby-dev"
}

resource "heroku_addon" "cloudinary" {
  app = heroku_app.itechart-auction.id
  plan = "cloudinary:starter"
}

resource "heroku_addon" "mailgun" {
  app = heroku_app.itechart-auction.id
  plan = "mailgun:starter"
}

resource "heroku_build" "itechart-auction" {
  app = heroku_app.itechart-auction.id

  source {
    path = "."
  }
}

resource "heroku_formation" "itechart-auction" {
  app = heroku_app.itechart-auction.id
  type = "web"
  quantity = 1
  size = "Free"
  depends_on = [
    heroku_build.itechart-auction
  ]
}

output "app_url" {
  value = heroku_app.itechart-auction.web_url
  description = "Application URL"
}