# s3-compare-action

This action allows comparing a remote S3-compatible bucket path to a local directory,
and returns a JSON list of files that are **not** present in the local directory.

### Why?

I am using this action to cheap out on Cloudflare workers paid/pro plan. I have an R2 bucket (S3-compatible),
and whenever I upload images in one of its directories, the images should also be committed to a GitHub repo containing a Hugo site. I also apply some formatting and resolution-setting to the downloaded images, but this is out of the scope of this repo.
