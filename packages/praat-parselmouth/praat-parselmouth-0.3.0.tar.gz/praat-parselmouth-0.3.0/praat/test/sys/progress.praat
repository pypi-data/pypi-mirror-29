writeInfoLine ("progress…")
sound1 = do ("Create Sound as pure tone...", "tone", 1, 0, 100, 44100, 440, 0.2, 0.01, 0.01)
stopwatch
pitch1 = do ("To Pitch...", 0, 75, 600)
appendInfoLine ("With progress bar: ", stopwatch)
sound2 = do ("Create Sound as pure tone...", "tone", 1, 0, 100, 44100, 440, 0.2, 0.01, 0.01)
stopwatch
pitch2 = noprogress do ("To Pitch...", 0, 75, 600)
appendInfoLine ("Without progress bar: ", stopwatch)
removeObject: sound1, pitch1, sound2, pitch2