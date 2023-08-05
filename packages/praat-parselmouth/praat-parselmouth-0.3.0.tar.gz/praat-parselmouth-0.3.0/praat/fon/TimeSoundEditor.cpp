/* TimeSoundEditor.cpp
 *
 * Copyright (C) 1992-2012,2013,2014,2015,2016,2017 Paul Boersma
 *
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This code is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this work. If not, see <http://www.gnu.org/licenses/>.
 */

#include "NUM2.h"
#include "TimeSoundEditor.h"
#include "EditorM.h"
#include "UnicodeData.h"

#include "enums_getText.h"
#include "TimeSoundEditor_enums.h"
#include "enums_getValue.h"
#include "TimeSoundEditor_enums.h"

Thing_implement (TimeSoundEditor, FunctionEditor, 0);

#include "prefs_define.h"
#include "TimeSoundEditor_prefs.h"
#include "prefs_install.h"
#include "TimeSoundEditor_prefs.h"
#include "prefs_copyToInstance.h"
#include "TimeSoundEditor_prefs.h"

#include <ciso646>

/********** Thing methods **********/

void structTimeSoundEditor :: v_destroy () noexcept {
	if (our d_ownSound)
		forget (our d_sound.data);
	NUMvector_free (d_sound.muteChannels, 1);
	TimeSoundEditor_Parent :: v_destroy ();
}

void structTimeSoundEditor :: v_info () {
	TimeSoundEditor_Parent :: v_info ();
	/* Sound flags: */
	MelderInfo_writeLine (U"Sound scaling strategy: ", kTimeSoundEditor_scalingStrategy_getText (p_sound_scalingStrategy));
}

/***** FILE MENU *****/

static void menu_cb_DrawVisibleSound (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Draw visible sound", nullptr)
		my v_form_pictureWindow (cmd);
		LABEL (U"Sound:")
		BOOLEAN (preserveTimes, U"Preserve times", my default_picture_preserveTimes ());
		REAL (bottom, U"left Vertical range", my default_picture_bottom ())
		REAL (top, U"right Vertical range", my default_picture_top ())
		my v_form_pictureMargins (cmd);
		my v_form_pictureSelection (cmd);
		BOOLEAN (garnish, U"Garnish", my default_picture_garnish ());
	EDITOR_OK
		my v_ok_pictureWindow (cmd);
		SET_BOOLEAN (preserveTimes, my pref_picture_preserveTimes ())
		SET_REAL (bottom,  my pref_picture_bottom ())
		SET_REAL (top,     my pref_picture_top ())
		my v_ok_pictureMargins (cmd);
		my v_ok_pictureSelection (cmd);
		SET_BOOLEAN (garnish, my pref_picture_garnish ())
	EDITOR_DO
		my v_do_pictureWindow (cmd);
		my pref_picture_preserveTimes () = preserveTimes;
		my pref_picture_bottom () = bottom;
		my pref_picture_top () = top;
		my v_do_pictureMargins (cmd);
		my v_do_pictureSelection (cmd);
		my pref_picture_garnish () = garnish;
		if (! my d_longSound.data && ! my d_sound.data)
			Melder_throw (U"There is no sound to draw.");
		autoSound publish = my d_longSound.data ?
			LongSound_extractPart (my d_longSound.data, my startWindow, my endWindow, my pref_picture_preserveTimes ()) :
			Sound_extractPart (my d_sound.data, my startWindow, my endWindow, kSound_windowShape::RECTANGULAR, 1.0, my pref_picture_preserveTimes ());
		Editor_openPraatPicture (me);
		Sound_draw (publish.get(), my pictureGraphics, 0.0, 0.0, my pref_picture_bottom (), my pref_picture_top (),
			my pref_picture_garnish (), U"Curve");
		FunctionEditor_garnish (me);
		Editor_closePraatPicture (me);
	EDITOR_END
}

static void menu_cb_DrawSelectedSound (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Draw selected sound", nullptr)
		my v_form_pictureWindow (cmd);
		LABEL (U"Sound:")
		BOOLEAN (preserveTimes, U"Preserve times",       my default_picture_preserveTimes ());
		REAL    (bottom,        U"left Vertical range",  my default_picture_bottom ());
		REAL    (top,           U"right Vertical range", my default_picture_top ());
		my v_form_pictureMargins (cmd);
		BOOLEAN (garnish, U"Garnish", my default_picture_garnish ());
	EDITOR_OK
		my v_ok_pictureWindow (cmd);
		SET_BOOLEAN (preserveTimes, my pref_picture_preserveTimes ());
		SET_REAL (bottom, my pref_picture_bottom ());
		SET_REAL (top,    my pref_picture_top ());
		my v_ok_pictureMargins (cmd);
		SET_BOOLEAN (garnish, my pref_picture_garnish ());
	EDITOR_DO
		my v_do_pictureWindow (cmd);
		my pref_picture_preserveTimes () = preserveTimes;
		my pref_picture_bottom () = bottom;
		my pref_picture_top () = top;
		my v_do_pictureMargins (cmd);
		my pref_picture_garnish () = garnish;
		if (! my d_longSound.data && ! my d_sound.data)
			Melder_throw (U"There is no sound to draw.");
		autoSound publish = my d_longSound.data ?
			LongSound_extractPart (my d_longSound.data, my startSelection, my endSelection, my pref_picture_preserveTimes ()) :
			Sound_extractPart (my d_sound.data, my startSelection, my endSelection, kSound_windowShape::RECTANGULAR, 1.0, my pref_picture_preserveTimes ());
		Editor_openPraatPicture (me);
		Sound_draw (publish.get(), my pictureGraphics, 0.0, 0.0, my pref_picture_bottom (), my pref_picture_top (),
			my pref_picture_garnish (), U"Curve");
		Editor_closePraatPicture (me);
	EDITOR_END
}

static void do_ExtractSelectedSound (TimeSoundEditor me, bool preserveTimes) {
	autoSound extract;
	if (my endSelection <= my startSelection)
		Melder_throw (U"No selection.");
	if (my d_longSound.data) {
		extract = LongSound_extractPart (my d_longSound.data, my startSelection, my endSelection, preserveTimes);
	} else if (my d_sound.data) {
		extract = Sound_extractPart (my d_sound.data, my startSelection, my endSelection, kSound_windowShape::RECTANGULAR, 1.0, preserveTimes);
	}
	Editor_broadcastPublication (me, extract.move());
}

static void menu_cb_ExtractSelectedSound_timeFromZero (TimeSoundEditor me, EDITOR_ARGS_DIRECT) {
	do_ExtractSelectedSound (me, false);
}

static void menu_cb_ExtractSelectedSound_preserveTimes (TimeSoundEditor me, EDITOR_ARGS_DIRECT) {
	do_ExtractSelectedSound (me, true);
}

static void menu_cb_ExtractSelectedSound_windowed (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Extract selected sound (windowed)", nullptr)
		WORD (name, U"Name", U"slice")
		OPTIONMENU_ENUM (windowShape, U"Window shape", kSound_windowShape, my default_extract_windowShape ())
		POSITIVE (relativeWidth, U"Relative width", my default_extract_relativeWidth ())
		BOOLEAN (preserveTimes, U"Preserve times", my default_extract_preserveTimes ())
	EDITOR_OK
		SET_ENUM (windowShape, kSound_windowShape, my pref_extract_windowShape ())
		SET_REAL (relativeWidth, my pref_extract_relativeWidth ())
		SET_BOOLEAN (preserveTimes, my pref_extract_preserveTimes ())
	EDITOR_DO
		Sound sound = my d_sound.data;
		Melder_assert (sound);
		my pref_extract_windowShape () = windowShape;
		my pref_extract_relativeWidth () = relativeWidth;
		my pref_extract_preserveTimes () = preserveTimes;
		autoSound extract = Sound_extractPart (sound, my startSelection, my endSelection, my pref_extract_windowShape (),
			my pref_extract_relativeWidth (), my pref_extract_preserveTimes ());
		Thing_setName (extract.get(), name);
		Editor_broadcastPublication (me, extract.move());
	EDITOR_END
}

static void menu_cb_ExtractSelectedSoundForOverlap (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Extract selected sound for overlap)", nullptr)
		WORD (name, U"Name", U"slice")
		POSITIVE (overlap, U"Overlap (s)", my default_extract_overlap ())
	EDITOR_OK
		SET_REAL (overlap, my pref_extract_overlap ())
	EDITOR_DO
		Sound sound = my d_sound.data;
		Melder_assert (sound);
		my pref_extract_overlap () = overlap;
		autoSound extract = Sound_extractPartForOverlap (sound, my startSelection, my endSelection,
			my pref_extract_overlap ());
		Thing_setName (extract.get(), name);
		Editor_broadcastPublication (me, extract.move());
	EDITOR_END
}

static void do_write (TimeSoundEditor me, MelderFile file, int format, int numberOfBitsPerSamplePoint) {
	if (my startSelection >= my endSelection)
		Melder_throw (U"No samples selected.");
	if (my d_longSound.data) {
		LongSound_savePartAsAudioFile (my d_longSound.data, format, my startSelection, my endSelection, file, numberOfBitsPerSamplePoint);
	} else if (my d_sound.data) {
		Sound sound = my d_sound.data;
		double margin = 0.0;
		integer nmargin = Melder_ifloor (margin / sound -> dx);
		integer first, last, numberOfSamples = Sampled_getWindowSamples (sound,
			my startSelection, my endSelection, & first, & last) + nmargin * 2;
		first -= nmargin;
		last += nmargin;
		if (numberOfSamples) {
			autoSound save = Sound_create (sound -> ny, 0.0, numberOfSamples * sound -> dx, numberOfSamples, sound -> dx, 0.5 * sound -> dx);
			integer offset = first - 1;
			if (first < 1) first = 1;
			if (last > sound -> nx) last = sound -> nx;
			for (integer channel = 1; channel <= sound -> ny; channel ++) {
				for (integer i = first; i <= last; i ++) {
					save -> z [channel] [i - offset] = sound -> z [channel] [i];
				}
			}
			Sound_saveAsAudioFile (save.get(), file, format, numberOfBitsPerSamplePoint);
		}
	}
}

static void menu_cb_WriteWav (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as WAV file", nullptr)
		Melder_sprint (defaultName,300, my d_longSound.data ? my d_longSound.data -> name : my d_sound.data -> name, U".wav");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_WAV, 16);
	EDITOR_END
}

static void menu_cb_SaveAs24BitWav (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as 24-bit WAV file", nullptr)
		Melder_assert (! my d_longSound.data && my d_sound.data);
		Melder_sprint (defaultName,300, my d_sound.data -> name, U".wav");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_WAV, 24);
	EDITOR_END
}

static void menu_cb_SaveAs32BitWav (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as 32-bit WAV file", nullptr)
		Melder_assert (! my d_longSound.data && my d_sound.data);
		Melder_sprint (defaultName,300, my d_sound.data -> name, U".wav");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_WAV, 32);
	EDITOR_END
}

static void menu_cb_WriteAiff (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as AIFF file", nullptr)
		Melder_sprint (defaultName,300, my d_longSound.data ? my d_longSound.data -> name : my d_sound.data -> name, U".aiff");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_AIFF, 16);
	EDITOR_END
}

static void menu_cb_WriteAifc (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as AIFC file", nullptr)
		Melder_sprint (defaultName,300, my d_longSound.data ? my d_longSound.data -> name : my d_sound.data -> name, U".aifc");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_AIFC, 16);
	EDITOR_END
}

static void menu_cb_WriteNextSun (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as NeXT/Sun file", nullptr)
		Melder_sprint (defaultName,300, my d_longSound.data ? my d_longSound.data -> name : my d_sound.data -> name, U".au");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_NEXT_SUN, 16);
	EDITOR_END
}

static void menu_cb_WriteNist (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as NIST file", nullptr)
		Melder_sprint (defaultName,300, my d_longSound.data ? my d_longSound.data -> name : my d_sound.data -> name, U".nist");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_NIST, 16);
	EDITOR_END
}

static void menu_cb_WriteFlac (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM_SAVE (U"Save selected sound as FLAC file", nullptr)
		Melder_sprint (defaultName,300, my d_longSound.data ? my d_longSound.data -> name : my d_sound.data -> name, U".flac");
	EDITOR_DO_SAVE
		do_write (me, file, Melder_FLAC, 16);
	EDITOR_END
}

void structTimeSoundEditor :: v_createMenuItems_file_draw (EditorMenu menu) {
	EditorMenu_addCommand (menu, U"Draw to picture window:", GuiMenu_INSENSITIVE, menu_cb_DrawVisibleSound /* dummy */);
	if (d_sound.data || d_longSound.data) {
		EditorMenu_addCommand (menu, U"Draw visible sound...", 0, menu_cb_DrawVisibleSound);
		drawButton = EditorMenu_addCommand (menu, U"Draw selected sound...", 0, menu_cb_DrawSelectedSound);
	}
}

void structTimeSoundEditor :: v_createMenuItems_file_extract (EditorMenu menu) {
	EditorMenu_addCommand (menu, U"Extract to objects window:", GuiMenu_INSENSITIVE, menu_cb_ExtractSelectedSound_preserveTimes /* dummy */);
	if (d_sound.data || d_longSound.data) {
		publishPreserveButton = EditorMenu_addCommand (menu, U"Extract selected sound (preserve times)", 0, menu_cb_ExtractSelectedSound_preserveTimes);
			EditorMenu_addCommand (menu, U"Extract sound selection (preserve times)", Editor_HIDDEN, menu_cb_ExtractSelectedSound_preserveTimes);
			EditorMenu_addCommand (menu, U"Extract selection (preserve times)", Editor_HIDDEN, menu_cb_ExtractSelectedSound_preserveTimes);
		publishButton = EditorMenu_addCommand (menu, U"Extract selected sound (time from 0)", 0, menu_cb_ExtractSelectedSound_timeFromZero);
			EditorMenu_addCommand (menu, U"Extract sound selection (time from 0)", Editor_HIDDEN, menu_cb_ExtractSelectedSound_timeFromZero);
			EditorMenu_addCommand (menu, U"Extract selection (time from 0)", Editor_HIDDEN, menu_cb_ExtractSelectedSound_timeFromZero);
			EditorMenu_addCommand (menu, U"Extract selection", Editor_HIDDEN, menu_cb_ExtractSelectedSound_timeFromZero);
		if (d_sound.data) {
			publishWindowButton = EditorMenu_addCommand (menu, U"Extract selected sound (windowed)...", 0, menu_cb_ExtractSelectedSound_windowed);
				EditorMenu_addCommand (menu, U"Extract windowed sound selection...", Editor_HIDDEN, menu_cb_ExtractSelectedSound_windowed);
				EditorMenu_addCommand (menu, U"Extract windowed selection...", Editor_HIDDEN, menu_cb_ExtractSelectedSound_windowed);
			publishOverlapButton = EditorMenu_addCommand (menu, U"Extract selected sound for overlap...", 0, menu_cb_ExtractSelectedSoundForOverlap);
		}
	}
}

void structTimeSoundEditor :: v_createMenuItems_file_write (EditorMenu menu) {
	EditorMenu_addCommand (menu, U"Save to disk:", GuiMenu_INSENSITIVE, menu_cb_WriteWav /* dummy */);
	if (d_sound.data || d_longSound.data) {
		writeWavButton = EditorMenu_addCommand (menu, U"Save selected sound as WAV file...", 0, menu_cb_WriteWav);
			EditorMenu_addCommand (menu, U"Write selected sound to WAV file...", Editor_HIDDEN, menu_cb_WriteWav);
			EditorMenu_addCommand (menu, U"Write sound selection to WAV file...", Editor_HIDDEN, menu_cb_WriteWav);
			EditorMenu_addCommand (menu, U"Write selection to WAV file...", Editor_HIDDEN, menu_cb_WriteWav);
		if (d_sound.data) {
			d_saveAs24BitWavButton = EditorMenu_addCommand (menu, U"Save selected sound as 24-bit WAV file...", 0, menu_cb_SaveAs24BitWav);
			d_saveAs32BitWavButton = EditorMenu_addCommand (menu, U"Save selected sound as 32-bit WAV file...", 0, menu_cb_SaveAs32BitWav);
		}
		writeAiffButton = EditorMenu_addCommand (menu, U"Save selected sound as AIFF file...", 0, menu_cb_WriteAiff);
			EditorMenu_addCommand (menu, U"Write selected sound to AIFF file...", Editor_HIDDEN, menu_cb_WriteAiff);
			EditorMenu_addCommand (menu, U"Write sound selection to AIFF file...", Editor_HIDDEN, menu_cb_WriteAiff);
			EditorMenu_addCommand (menu, U"Write selection to AIFF file...", Editor_HIDDEN, menu_cb_WriteAiff);
		writeAifcButton = EditorMenu_addCommand (menu, U"Save selected sound as AIFC file...", 0, menu_cb_WriteAifc);
			EditorMenu_addCommand (menu, U"Write selected sound to AIFC file...", Editor_HIDDEN, menu_cb_WriteAifc);
			EditorMenu_addCommand (menu, U"Write sound selection to AIFC file...", Editor_HIDDEN, menu_cb_WriteAifc);
			EditorMenu_addCommand (menu, U"Write selection to AIFC file...", Editor_HIDDEN, menu_cb_WriteAifc);
		writeNextSunButton = EditorMenu_addCommand (menu, U"Save selected sound as Next/Sun file...", 0, menu_cb_WriteNextSun);
			EditorMenu_addCommand (menu, U"Write selected sound to Next/Sun file...", Editor_HIDDEN, menu_cb_WriteNextSun);
			EditorMenu_addCommand (menu, U"Write sound selection to Next/Sun file...", Editor_HIDDEN, menu_cb_WriteNextSun);
			EditorMenu_addCommand (menu, U"Write selection to Next/Sun file...", Editor_HIDDEN, menu_cb_WriteNextSun);
		writeNistButton = EditorMenu_addCommand (menu, U"Save selected sound as NIST file...", 0, menu_cb_WriteNist);
			EditorMenu_addCommand (menu, U"Write selected sound to NIST file...", Editor_HIDDEN, menu_cb_WriteNist);
			EditorMenu_addCommand (menu, U"Write sound selection to NIST file...", Editor_HIDDEN, menu_cb_WriteNist);
			EditorMenu_addCommand (menu, U"Write selection to NIST file...", Editor_HIDDEN, menu_cb_WriteNist);
		writeFlacButton = EditorMenu_addCommand (menu, U"Save selected sound as FLAC file...", 0, menu_cb_WriteFlac);
			EditorMenu_addCommand (menu, U"Write selected sound to FLAC file...", Editor_HIDDEN, menu_cb_WriteFlac);
			EditorMenu_addCommand (menu, U"Write sound selection to FLAC file...", Editor_HIDDEN, menu_cb_WriteFlac);
	}
}

void structTimeSoundEditor :: v_createMenuItems_file (EditorMenu menu) {
	TimeSoundEditor_Parent :: v_createMenuItems_file (menu);
	v_createMenuItems_file_draw (menu);
	EditorMenu_addCommand (menu, U"-- after file draw --", 0, nullptr);
	v_createMenuItems_file_extract (menu);
	EditorMenu_addCommand (menu, U"-- after file extract --", 0, nullptr);
	v_createMenuItems_file_write (menu);
	EditorMenu_addCommand (menu, U"-- after file write --", 0, nullptr);
}

/********** QUERY MENU **********/

static void menu_cb_SoundInfo (TimeSoundEditor me, EDITOR_ARGS_DIRECT) {
	Thing_info (my d_sound.data);
}

static void menu_cb_LongSoundInfo (TimeSoundEditor me, EDITOR_ARGS_DIRECT) {
	Thing_info (my d_longSound.data);
}

void structTimeSoundEditor :: v_createMenuItems_query_info (EditorMenu menu) {
	TimeSoundEditor_Parent :: v_createMenuItems_query_info (menu);
	if (d_sound.data && d_sound.data != data) {
		EditorMenu_addCommand (menu, U"Sound info", 0, menu_cb_SoundInfo);
	} else if (d_longSound.data && d_longSound.data != data) {
		EditorMenu_addCommand (menu, U"LongSound info", 0, menu_cb_LongSoundInfo);
	}
}

/********** VIEW MENU **********/

static void menu_cb_soundScaling (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Sound scaling", nullptr)
		OPTIONMENU_ENUM (scalingStrategy, U"Scaling strategy", kTimeSoundEditor_scalingStrategy, my default_sound_scalingStrategy ())
		LABEL (U"For \"fixed height\":")
		POSITIVE (height, U"Height", my default_sound_scaling_height ())
		LABEL (U"For \"fixed range\":")
		REAL (minimum, U"Minimum", my default_sound_scaling_minimum ())
		REAL (maximum, U"Maximum", my default_sound_scaling_maximum ())
	EDITOR_OK
		SET_ENUM (scalingStrategy, kTimeSoundEditor_scalingStrategy, my p_sound_scalingStrategy)
		SET_REAL (height,  my p_sound_scaling_height)
		SET_REAL (minimum, my p_sound_scaling_minimum)
		SET_REAL (maximum, my p_sound_scaling_maximum)
	EDITOR_DO
		my pref_sound_scalingStrategy () = my p_sound_scalingStrategy = scalingStrategy;
		my pref_sound_scaling_height  () = my p_sound_scaling_height  = height;
		my pref_sound_scaling_minimum () = my p_sound_scaling_minimum = minimum;
		my pref_sound_scaling_maximum () = my p_sound_scaling_maximum = maximum;
		FunctionEditor_redraw (me);
	EDITOR_END
}

static void menu_cb_soundMuteChannels (TimeSoundEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Mute channels", nullptr)
		TEXTFIELD (channels_string, U"Channels", U"2")
	EDITOR_OK
	EDITOR_DO
		integer numberOfChannels = my d_longSound.data ? my d_longSound.data -> numberOfChannels : my d_sound.data -> ny;
		integer numberOfElements;
		autoNUMvector<integer> channelNumber (NUMstring_getElementsOfRanges (channels_string, 5 * numberOfChannels, & numberOfElements, nullptr, U"channel", false), 1);
		bool *muteChannels = my d_sound.muteChannels;
		for (integer i = 1; i <= numberOfChannels; i ++) {
			muteChannels [i] = false;
		}
		for (integer i = 1; i <= numberOfElements; i++) {
			if (channelNumber [i] > 0 && channelNumber [i] <= numberOfChannels) {
				muteChannels [channelNumber [i]] = true;
			}
		}
		FunctionEditor_redraw (me);
	EDITOR_END
}

void structTimeSoundEditor :: v_createMenuItems_view (EditorMenu menu) {
	if (d_sound.data || d_longSound.data)
		v_createMenuItems_view_sound (menu);
	TimeSoundEditor_Parent :: v_createMenuItems_view (menu);
}

void structTimeSoundEditor :: v_createMenuItems_view_sound (EditorMenu menu) {
	EditorMenu_addCommand (menu, U"Sound scaling...", 0, menu_cb_soundScaling);
	EditorMenu_addCommand (menu, U"Mute channels...", 0, menu_cb_soundMuteChannels);
}

void structTimeSoundEditor :: v_updateMenuItems_file () {
	Sampled sound;
	if (d_sound.data) {
		sound = d_sound.data;
	} else {
		sound = d_longSound.data;
	}
	if (! sound) return;
	integer first, last, selectedSamples = Sampled_getWindowSamples (sound, our startSelection, our endSelection, & first, & last);
	if (drawButton) {
		GuiThing_setSensitive (drawButton, selectedSamples != 0);
		GuiThing_setSensitive (publishButton, selectedSamples != 0);
		GuiThing_setSensitive (publishPreserveButton, selectedSamples != 0);
		if (publishWindowButton) GuiThing_setSensitive (publishWindowButton, selectedSamples != 0);
		if (publishOverlapButton) GuiThing_setSensitive (publishOverlapButton, selectedSamples != 0);
	}
	GuiThing_setSensitive (writeWavButton, selectedSamples != 0);
	if (d_saveAs24BitWavButton)
		GuiThing_setSensitive (d_saveAs24BitWavButton, selectedSamples != 0);
	if (d_saveAs32BitWavButton)
		GuiThing_setSensitive (d_saveAs32BitWavButton, selectedSamples != 0);
	GuiThing_setSensitive (writeAiffButton, selectedSamples != 0);
	GuiThing_setSensitive (writeAifcButton, selectedSamples != 0);
	GuiThing_setSensitive (writeNextSunButton, selectedSamples != 0);
	GuiThing_setSensitive (writeNistButton, selectedSamples != 0);
	GuiThing_setSensitive (writeFlacButton, selectedSamples != 0);
}

void TimeSoundEditor_drawSound (TimeSoundEditor me, double globalMinimum, double globalMaximum) {
	Sound sound = my d_sound.data;
	LongSound longSound = my d_longSound.data;
	Melder_assert (!! sound != !! longSound);
	int nchan = sound ? sound -> ny : longSound -> numberOfChannels;
	bool cursorVisible = my startSelection == my endSelection && my startSelection >= my startWindow && my startSelection <= my endWindow;
	Graphics_setColour (my graphics.get(), Graphics_BLACK);
	bool fits;
	try {
		fits = sound ? true : LongSound_haveWindow (longSound, my startWindow, my endWindow);
	} catch (MelderError) {
		bool outOfMemory = !! str32str (Melder_getError (), U"memory");
		if (Melder_debug == 9) Melder_flushError (); else Melder_clearError ();
		Graphics_setWindow (my graphics.get(), 0.0, 1.0, 0.0, 1.0);
		Graphics_setTextAlignment (my graphics.get(), Graphics_CENTRE, Graphics_HALF);
		Graphics_text (my graphics.get(), 0.5, 0.5, outOfMemory ? U"(out of memory)" : U"(cannot read sound file)");
		return;
	}
	if (! fits) {
		Graphics_setWindow (my graphics.get(), 0.0, 1.0, 0.0, 1.0);
		Graphics_setTextAlignment (my graphics.get(), Graphics_CENTRE, Graphics_HALF);
		Graphics_text (my graphics.get(), 0.5, 0.5, U"(window too large; zoom in to see the data)");
		return;
	}
	integer first, last;
	if (Sampled_getWindowSamples (sound ? (Sampled) sound : (Sampled) longSound, my startWindow, my endWindow, & first, & last) <= 1) {
		Graphics_setWindow (my graphics.get(), 0.0, 1.0, 0.0, 1.0);
		Graphics_setTextAlignment (my graphics.get(), Graphics_CENTRE, Graphics_HALF);
		Graphics_text (my graphics.get(), 0.5, 0.5, U"(zoom out to see the data)");
		return;
	}
	const int numberOfVisibleChannels = nchan > 8 ? 8 : nchan;
	const int firstVisibleChannel = my d_sound.channelOffset + 1;
	int lastVisibleChannel = my d_sound.channelOffset + numberOfVisibleChannels;
	if (lastVisibleChannel > nchan) lastVisibleChannel = nchan;
	double maximumExtent = 0.0, visibleMinimum = 0.0, visibleMaximum = 0.0;
	if (my p_sound_scalingStrategy == kTimeSoundEditor_scalingStrategy::BY_WINDOW) {
		if (longSound)
			LongSound_getWindowExtrema (longSound, my startWindow, my endWindow, firstVisibleChannel, & visibleMinimum, & visibleMaximum);
		else
			Matrix_getWindowExtrema (sound, first, last, firstVisibleChannel, firstVisibleChannel, & visibleMinimum, & visibleMaximum);
		for (int ichan = firstVisibleChannel + 1; ichan <= lastVisibleChannel; ichan ++) {
			double visibleChannelMinimum, visibleChannelMaximum;
			if (longSound)
				LongSound_getWindowExtrema (longSound, my startWindow, my endWindow, ichan, & visibleChannelMinimum, & visibleChannelMaximum);
			else
				Matrix_getWindowExtrema (sound, first, last, ichan, ichan, & visibleChannelMinimum, & visibleChannelMaximum);
			if (visibleChannelMinimum < visibleMinimum)
				visibleMinimum = visibleChannelMinimum;
			if (visibleChannelMaximum > visibleMaximum)
				visibleMaximum = visibleChannelMaximum;
		}
		maximumExtent = visibleMaximum - visibleMinimum;
	}
	for (int ichan = firstVisibleChannel; ichan <= lastVisibleChannel; ichan ++) {
		double cursorFunctionValue = longSound ? 0.0 :
			Vector_getValueAtX (sound, 0.5 * (my startSelection + my endSelection), ichan, 70);
		/*
		 * BUG: this will only work for mono or stereo, until Graphics_function16 handles quadro.
		 */
		double ymin = (double) (numberOfVisibleChannels - ichan + my d_sound.channelOffset) / numberOfVisibleChannels;
		double ymax = (double) (numberOfVisibleChannels + 1 - ichan + my d_sound.channelOffset) / numberOfVisibleChannels;
		Graphics_Viewport vp = Graphics_insetViewport (my graphics.get(), 0.0, 1.0, ymin, ymax);
		bool horizontal = false;
		double minimum = sound ? globalMinimum : -1.0, maximum = sound ? globalMaximum : 1.0;
		if (my p_sound_scalingStrategy == kTimeSoundEditor_scalingStrategy::BY_WINDOW) {
			if (nchan > 2) {
				if (longSound) {
					LongSound_getWindowExtrema (longSound, my startWindow, my endWindow, ichan, & minimum, & maximum);
				} else {
					Matrix_getWindowExtrema (sound, first, last, ichan, ichan, & minimum, & maximum);
				}
				if (maximumExtent > 0.0) {
					double middle = 0.5 * (minimum + maximum);
					minimum = middle - 0.5 * maximumExtent;
					maximum = middle + 0.5 * maximumExtent;
				}
			} else {
				minimum = visibleMinimum;
				maximum = visibleMaximum;
			}
		} else if (my p_sound_scalingStrategy == kTimeSoundEditor_scalingStrategy::BY_WINDOW_AND_CHANNEL) {
			if (longSound) {
				LongSound_getWindowExtrema (longSound, my startWindow, my endWindow, ichan, & minimum, & maximum);
			} else {
				Matrix_getWindowExtrema (sound, first, last, ichan, ichan, & minimum, & maximum);
			}
		} else if (my p_sound_scalingStrategy == kTimeSoundEditor_scalingStrategy::FIXED_HEIGHT) {
			if (longSound) {
				LongSound_getWindowExtrema (longSound, my startWindow, my endWindow, ichan, & minimum, & maximum);
			} else {
				Matrix_getWindowExtrema (sound, first, last, ichan, ichan, & minimum, & maximum);
			}
			double channelExtent = my p_sound_scaling_height;
			double middle = 0.5 * (minimum + maximum);
			minimum = middle - 0.5 * channelExtent;
			maximum = middle + 0.5 * channelExtent;
		} else if (my p_sound_scalingStrategy == kTimeSoundEditor_scalingStrategy::FIXED_RANGE) {
			minimum = my p_sound_scaling_minimum;
			maximum = my p_sound_scaling_maximum;
		}
		if (minimum == maximum) { horizontal = true; minimum -= 1.0; maximum += 1.0;}
		Graphics_setWindow (my graphics.get(), my startWindow, my endWindow, minimum, maximum);
		if (horizontal) {
			Graphics_setTextAlignment (my graphics.get(), Graphics_RIGHT, Graphics_HALF);
			double mid = 0.5 * (minimum + maximum);
			Graphics_text (my graphics.get(), my startWindow, mid, Melder_float (Melder_half (mid)));
		} else {
			if (! cursorVisible || isundef (cursorFunctionValue) || Graphics_dyWCtoMM (my graphics.get(), cursorFunctionValue - minimum) > 5.0) {
				Graphics_setTextAlignment (my graphics.get(), Graphics_RIGHT, Graphics_BOTTOM);
				Graphics_text (my graphics.get(), my startWindow, minimum, Melder_float (Melder_half (minimum)));
			}
			if (! cursorVisible || isundef (cursorFunctionValue) || Graphics_dyWCtoMM (my graphics.get(), maximum - cursorFunctionValue) > 5.0) {
				Graphics_setTextAlignment (my graphics.get(), Graphics_RIGHT, Graphics_TOP);
				Graphics_text (my graphics.get(), my startWindow, maximum, Melder_float (Melder_half (maximum)));
			}
		}
		if (minimum < 0 && maximum > 0 && ! horizontal) {
			Graphics_setWindow (my graphics.get(), 0.0, 1.0, minimum, maximum);
			if (! cursorVisible || isundef (cursorFunctionValue) || fabs (Graphics_dyWCtoMM (my graphics.get(), cursorFunctionValue - 0.0)) > 3.0) {
				Graphics_setTextAlignment (my graphics.get(), Graphics_RIGHT, Graphics_HALF);
				Graphics_text (my graphics.get(), 0.0, 0.0, U"0");
			}
			Graphics_setColour (my graphics.get(), Graphics_CYAN);
			Graphics_setLineType (my graphics.get(), Graphics_DOTTED);
			Graphics_line (my graphics.get(), 0.0, 0.0, 1.0, 0.0);
			Graphics_setLineType (my graphics.get(), Graphics_DRAWN);
		}
		/*
		 * Garnish the drawing area of each channel.
		 */
		Graphics_setWindow (my graphics.get(), 0.0, 1.0, 0.0, 1.0);
		Graphics_setColour (my graphics.get(), Graphics_CYAN);
		Graphics_innerRectangle (my graphics.get(), 0.0, 1.0, 0.0, 1.0);
		Graphics_setColour (my graphics.get(), Graphics_BLACK);
		if (nchan > 1) {
			Graphics_setTextAlignment (my graphics.get(), Graphics_LEFT, Graphics_HALF);
			Graphics_setTextAlignment (my graphics.get(), Graphics_LEFT, Graphics_HALF);
			const char32 *channelName = my v_getChannelName (ichan);
			static MelderString channelLabel { };
			MelderString_copy (& channelLabel, ( channelName ? U"ch" : U"Ch " ), ichan);
			if (channelName)
				MelderString_append (& channelLabel, U": ", channelName);
			//
			MelderString_append (& channelLabel, U" ",
				( my d_sound.muteChannels [ichan] ? UNITEXT_SPEAKER_WITH_CANCELLATION_STROKE : UNITEXT_SPEAKER ));
			if (ichan > 8 && ichan - my d_sound.channelOffset == 1) {
				MelderString_append (& channelLabel, U"      " UNITEXT_UPWARDS_ARROW);
			} else if (ichan >= 8 && ichan - my d_sound.channelOffset == 8 && ichan < nchan) {
				MelderString_append (& channelLabel, U"      " UNITEXT_DOWNWARDS_ARROW);
			}
			Graphics_text (my graphics.get(), 1.0, 0.5, channelLabel.string);
		}
		/*
		 * Draw a very thin separator line underneath.
		 */
		if (ichan < nchan) {
			/*Graphics_setColour (my graphics.get(), Graphics_BLACK);*/
			Graphics_line (my graphics.get(), 0.0, 0.0, 1.0, 0.0);
		}
		/*
		 * Draw the samples.
		 */
		/*if (ichan == 1) FunctionEditor_SoundAnalysis_drawPulses (this);*/
		if (sound) {
			Graphics_setWindow (my graphics.get(), my startWindow, my endWindow, minimum, maximum);
			if (cursorVisible && isdefined (cursorFunctionValue))
				FunctionEditor_drawCursorFunctionValue (me, cursorFunctionValue, Melder_float (Melder_half (cursorFunctionValue)), U"");
			Graphics_setColour (my graphics.get(), Graphics_BLACK);
			Graphics_function (my graphics.get(), sound -> z [ichan], first, last,
				Sampled_indexToX (sound, first), Sampled_indexToX (sound, last));
		} else {
			Graphics_setWindow (my graphics.get(), my startWindow, my endWindow, minimum * 32768, maximum * 32768);
			Graphics_function16 (my graphics.get(),
				longSound -> buffer - longSound -> imin * nchan + (ichan - 1), nchan - 1, first, last,
				Sampled_indexToX (longSound, first), Sampled_indexToX (longSound, last));
		}
		Graphics_resetViewport (my graphics.get(), vp);
	}
	Graphics_setWindow (my graphics.get(), 0.0, 1.0, 0.0, 1.0);
	Graphics_rectangle (my graphics.get(), 0.0, 1.0, 0.0, 1.0);
}

bool structTimeSoundEditor :: v_click (double xbegin, double ybegin, bool shiftKeyPressed) {
	Sound sound = d_sound.data;
	LongSound longSound = d_longSound.data;
	if (!! sound != !! longSound) {
		ybegin = (ybegin - v_getBottomOfSoundArea ()) / (1.0 - v_getBottomOfSoundArea ());
		int nchan = sound ? sound -> ny : longSound -> numberOfChannels;
		if (nchan > 8) {
			trace (xbegin, U" ", ybegin, U" ", nchan, U" ", d_sound.channelOffset);
			if (xbegin >= our endWindow && ybegin > 0.875 && ybegin <= 1.000 && d_sound.channelOffset > 0) {
				d_sound.channelOffset -= 8;
				return FunctionEditor_UPDATE_NEEDED;
			}
			if (xbegin >= our endWindow && ybegin > 0.000 && ybegin <= 0.125 && d_sound.channelOffset < nchan - 8) {
				d_sound.channelOffset += 8;
				return FunctionEditor_UPDATE_NEEDED;
			}
		}
	}
	return TimeSoundEditor_Parent :: v_click (xbegin, ybegin, shiftKeyPressed);
}

bool structTimeSoundEditor :: v_clickB (double xbegin, double ybegin) {
	Sound sound = d_sound.data;
	LongSound longSound = d_longSound.data;
	if (!! sound != !! longSound) {
		ybegin = (ybegin - v_getBottomOfSoundArea ()) / (1.0 - v_getBottomOfSoundArea ());
		int numberOfChannels = sound ? sound -> ny : longSound -> numberOfChannels;
		if (numberOfChannels > 1) {
			int numberOfVisibleChannels = numberOfChannels > 8 ? 8 : numberOfChannels;
			bool *muteChannels = d_sound . muteChannels;
			trace (xbegin, U" ", ybegin, U" ", numberOfChannels, U" ", d_sound.channelOffset);
			int box = ybegin * numberOfVisibleChannels + 1;
			box = box < 1 ? 1 : box > numberOfVisibleChannels ? numberOfVisibleChannels : box; // top: numberOfVisibleChannels, bottom: 1
			int channel = numberOfVisibleChannels - box + 1 + d_sound.channelOffset;
			if (Melder_debug == 24) {
				Melder_casual (U"structTimeSoundEditor :: v_clickB ", ybegin, U" ", channel);
			}
			muteChannels [channel] = not muteChannels [channel];
			return FunctionEditor_UPDATE_NEEDED;
		}
	}
	return TimeSoundEditor_Parent :: v_clickB (xbegin, ybegin);
}

void TimeSoundEditor_init (TimeSoundEditor me, const char32 *title, Function data, Sampled sound, bool ownSound) {
	my d_ownSound = ownSound;
	if (sound) {
		integer numberOfChannels = 1;
		if (ownSound) {
			Melder_assert (Thing_isa (sound, classSound));
			my d_sound.data = Data_copy ((Sound) sound).releaseToAmbiguousOwner();   // deep copy; ownership transferred
			Matrix_getWindowExtrema (my d_sound.data, 1, my d_sound.data -> nx, 1, my d_sound.data -> ny, & my d_sound.minimum, & my d_sound.maximum);
			numberOfChannels = my d_sound.data -> ny;
		} else if (Thing_isa (sound, classSound)) {
			my d_sound.data = (Sound) sound;   // reference copy; ownership not transferred
			Matrix_getWindowExtrema (my d_sound.data, 1, my d_sound.data -> nx, 1, my d_sound.data -> ny, & my d_sound.minimum, & my d_sound.maximum);
			numberOfChannels = my d_sound.data -> ny;
		} else if (Thing_isa (sound, classLongSound)) {
			my d_longSound.data = (LongSound) sound;
			my d_sound.minimum = -1.0, my d_sound.maximum = 1.0;
			numberOfChannels = my d_longSound.data -> numberOfChannels;
		} else {
			Melder_fatal (U"Invalid sound class in TimeSoundEditor::init.");
		}
		my d_sound.muteChannels = NUMvector<bool> (1, numberOfChannels);
	}
	FunctionEditor_init (me, title, data);
}

/* End of file TimeSoundEditor.cpp */
