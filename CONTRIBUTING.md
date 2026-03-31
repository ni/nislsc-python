# Contributing to nislsc

Contributions to **nislsc** are welcome from all!

**nislsc** is managed via [git](https://git-scm.com), with the canonical upstream repository hosted on [GitHub](https://github.com/ni/<reponame>/).

**nislsc** follows a pull-request model for development.  If you wish to contribute, you will need to create a GitHub account, fork this project, push a branch with your changes to your project, and then submit a pull request.

Please remember to sign off your commits (e.g., by using `git commit -s` if you are using the command line client). This amends your git commit message with a line of the form `Signed-off-by: Name Lastname <name.lastmail@emailaddress.com>`. Please include all authors of any given commit into the commit message with a `Signed-off-by` line. This indicates that you have read and signed the Developer Certificate of Origin (see below) and are able to legally submit your code to this repository.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/) for more details.

## Getting Started

- TODO: include build steps here.

## Testing

- TODO: include testing steps here.

## Building Documentation

- TODO: include documentation steps here.

## Branching Policy

Active development for the next release occurs on the `main` branch.

During finalization, we create a release branch (e.g. `releases/1.2`) in order to control which changes target the imminent release vs. the next release after that. Changes that are intended for both the imminent release and subsequent releases should be made in the `main` branch and cherry-picked into the release branch. Changes that only apply to the imminent release (such as version numbers) may be made directly in the release branch.

## Release Process

**Versioning**
- This project follows Semantic Versioning principles.
- Versions take the form MAJOR.MINOR.PATCH.
- MINOR is bumped for most quarterly releases because new features are typically introduced without breaking compatibility.<br>
  Example: `0.1.0 → 0.2.0`
- PATCH is bumped for releases that contain only bug fixes and/or dependency updates.<br>
  Example: `0.1.0 → 0.1.1`
- MAJOR is bumped only when making breaking changes.
  * During `0.x` development, breaking changes are allowed at any time without a major bump. This is expected for pre‑1.0 projects.
  * Once the project reaches `1.x`, breaking changes must trigger a major version increment.

**Release Branches**
- For each new release, create a corresponding release branch so patches can be released to it if needed.
- Release branches are named in the form `releases/MAJOR.MINOR`.<br>
  Example: `releases/0.1`
- The release branch may be created before the official release, allowing changes for the next release to be merged into `main` branch.
- Patch fixes for an existing release should be cherry‑picked into the appropriate release branch.

**Tagging**
- Git tags for pre-releases are version numbers in the form `1.2.3.dev4`.
- Git tags for releases are version numbers in the form `1.2 or 1.2.3`.
- This project does not prefix Git tags with the letter `v`.

**Publishing**
- This GitHub repository has an automated workflow for publishing packages
  to PyPi and publishing documentation to GitHub Pages.
- This automated workflow is initiated by manually creating a new release in the GitHub web UI:
  1. On the releases page, click **Draft a new release**.
  2. Choose a tag for the new release, based on the desired version number.
     The publish workflow will validate that the version number in `pyproject.toml` matches this tag.
  3. Choose the appropriate target branch for the new release:
     * Early pre-releases should be released from `main`.
     * Late pre-releases and official releases should be released from a release branch such as
       `releases/1.2`.
  4. If it is a pre-release, check **Set as a pre-release**. If it is an official release,
     uncheck **Set as a pre-release** and check **Set as the latest release**.
  5. Release notes can be copied from the most recent entry in CHANGELOG.md corresponding to the version being released.
  6. Click **Save draft**. Consider sharing the link to the draft release with the other repo maintainers.
  7. Once the versions and release notes are ready, click **Publish release**.
  8. Publishing a release automatically triggers the [publish.yml](https://github.com/ni/nislsc-python/blob/main/.github/workflows/publish.yml)
     workflow, which checks and builds the package, requests approval to publish it using the `pypi` deployment environment, and
     publishes the package to PyPi using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/).
  9. GitHub contacts the approvers of the `pypi` deployment environment. One of them must approve the deployment for the publishing to proceed.
- In between official releases, publish pre-releases for internal testing.
  * Pre-releases use version numbers such as `0.2.0.dev0`.
  * Pre-releases should be marked as **Set as a pre-release** in GitHub so they do not show up as the latest version in GitHub's Releases page.
- The `.devN` suffix is removed only when making an official release for external users, typically once per quarter.
- Once the automated workflow completes successfully, check that the new version is visible in this location:
  * [https://pypi.org/project/nislsc/#history](https://pypi.org/project/nislsc/#history).
- The automated workflow will create a PR with a title like "chore: Update project versions".
  * Close and re-open the PR to run checks, as a workaround for
    [https://github.com/ni/python-actions/issues/6](https://github.com/ni/python-actions/issues/6). Then, review and merge the PR.

**Cherry-Picking**
- To cherry-pick a change into a release branch:
  * Make sure the PR submitting the change to the `main` branch is completed.
  * Check out the target release branch and create a dev branch.
  * Run `git log main` and find the commit id for the merged PR (not your dev branch commit id).
  * Run `git cherry-pick -x <commit-id>`. If there are conflicts, resolve them and re-test.
    + `-x` includes `(cherry picked from commit <commit-id>)` in the commit description.
  * Push the dev branch to GitHub and create a PR.
    + Prefix the title with `[releases/N.N]` where N.N is the release branch version.
    + Include a link to the original PR in the description.

## Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/ni/nislsc-python/blob/main/LICENSE)
for details about how **nislsc** is licensed.
