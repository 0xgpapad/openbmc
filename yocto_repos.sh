branches=(
    rocko
    lf-master
    lf-dunfell
    lf-honister
)

rocko_repos=(
    meta-openembedded:eae996301
    meta-security:74860b2
    poky:5f660914cd # bitbake: bitbake-user-manual: Fixed section head typo
)
rocko_poky_patch="0001-rocko-backport-support-for-override.patch"
lf_master_repos=(
    lf-openbmc:9a2a1dade
)
lf_dunfell_repos=(
    lf-openbmc:fff6b3483
)
lf_honister_repos=(
    lf-openbmc:415294223
)
