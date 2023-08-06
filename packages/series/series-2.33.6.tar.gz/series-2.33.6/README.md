### Changelog

# 2.24
* Client command `purge`, taking as arguments a number of days (default 30),
  deleting all downloaded releases older than that.

# 2.23
* Add `search_name` field to releases and shows that is used for torrent
  search. Defaults to the tvdb name.
* Client command `activate_show`, analogous to `activate_release`.

# 2.22
* Before scheduling a release, the airdate is double-checked in anticipation of
  tv program rescheduling.

# 2.21
* When adding shows using `seriesgetc add_show`, the supplied name is matched
  against TVDB and the user is queried to choose a candidate for the show.

# 2.20
* Shows and releases now have the attribute `downgrade_after`, given in hours.
  If a release has not found any torrents or could not be cached after that
  amount of hours, it is downgraded to standard definition and searched again.
  The attribute can be set via the client commands `update_show` and
  `update_release.`

# 2.17
* Use subprocess for the downloader, avoiding blocking during downloads.

# 2.14
* Config option `min_seeders`: Search result with less seeders than this value
  are ignored.

# 2.13
* Search results are now accepted if they have a year as a suffix to the show
  name, like *The Americans 2013 S03E01*

# 2.10
* When creating a release from cli, the airdate is queried and set.
* *Client command `set_airdate`:* Takes a date in the shape `[YYYY-]MM-DD` and
  applies it to the selected release.

# 2.8
* *Client command `explain_show`:* Analog to `explain`, for shows.

# 2.6
* *Client command `explain`:* Prints information about a release monitor's
  state. For each handler (optionally selected by the last parameter), the
  exact boolean term indicating the monitor's qualification for handling is
  shown, atomic conditions (e.g. `downloaded`) being marked in red or green,
  depending on whether it blocks or allows handling.

# 2.5
* *Client command `activate_release`:* Resets the cooldown of the specified
  monitor, which prevents a failed release from being reprocessed immediately
  and can take up to 24 hours (in the show scheduler)

# 2.4
* *Client command `update_release`:* The specified key=value arguments are set
  on the release monitor matching the episode selector, for example:

  `seriesgetc update_release series_name 5 3 archived=0 resolutions=1080p,720p`

# 2.3
* *Resolutions*: A release monitor now has a list of accepted resolutions that
will be searched for in order. The global default is to use `1080p,720p` if the
config option `full_hd` in `[get]` is `True` or `720p` if not. The empty string
is an SD release, it can be appended to specific resolutions like this:
`1080p,`
