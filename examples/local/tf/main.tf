resource "random_string" "random" {
  length           = 16
  special          = true
  override_special = "/@£$"
}

variable "input" {
    description = "input test"
}

output "input" {
    value = "output-${var.input}"
}

output "a_string" {
    value = random_string.random.result
}