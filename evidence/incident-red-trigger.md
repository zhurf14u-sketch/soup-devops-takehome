# Intentional red-run trigger

This file exists solely to trigger the four expected-red GitHub Actions jobs. The
jobs execute against the immutable `reproductions/naive` fixture and must fail.
They are evidence of the incident, not failures of the corrected release pipeline.
