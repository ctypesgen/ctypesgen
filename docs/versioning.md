## Versioning

Versioning within ctypesgen follows these general rules:

* Versions are all defined with specific reference to a commit that is relative
  to a Git tag.
* Versions numbers include enough information to find the exact commit that
  represents the version release.
* All tags should follow the format of:  x.y.z
    * x : Major revision with major differences of capabilities as compared to
          other major revisions.  The definition of "major capabilities" is a
          somewhat subjective concept, dependent on the developers.
    * y : Minor revision with incompatible differences of interfaces as compared
          to earlier revisions.  Interfaces that are considered to impact the
          minor revision number are external interfaces such as the command line
          or perhaps python version support.
    * z : Micro revision indicating a general acceptance of multiple patches
          since last tag. This number may be used to help mark minor development
          milestones.

By using the Git command ‘git describe‘, a unique identifier of the full version
string can be shown as:

  * x.y.z[-n-g*sha1*]
    where [-n-g*sha1*] shows up *automatically* if changes have been made since
    the last tag
  * n : Indicates the number of commits since the last tag
  * g*sha1*: Indicates the abreviated SHA1 hash of the latest commit

Thus, the version *1.0.0-2* means that the last tag before that version was
*1.0.0* and the version *1.0.0-2* is exactly 2 commits after the tag *1.0.0*.

To re-baseline the [-n-g*sha1*] portion showing up in "git describe" (i.e.
remove it until another commit is added), we simply add another tag following
the *x.y.z* format.
