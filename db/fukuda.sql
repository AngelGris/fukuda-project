CREATE TABLE `images` (
  `id` int(10) UNSIGNED NOT NULL,
  `hexa` char(6) COLLATE utf8_bin NOT NULL,
  `red` tinyint(3) UNSIGNED NOT NULL,
  `green` tinyint(3) UNSIGNED NOT NULL,
  `blue` tinyint(3) UNSIGNED NOT NULL,
  `priority` tinyint(1) UNSIGNED NOT NULL,
  `used` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

ALTER TABLE `images`
  ADD PRIMARY KEY (`id`);