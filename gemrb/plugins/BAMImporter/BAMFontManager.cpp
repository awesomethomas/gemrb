/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2011 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 *
 */

#include "BAMFont.h"
#include "BAMFontManager.h"
#include "Palette.h"
#include "Sprite2D.h"

using namespace GemRB;

BAMFontManager::~BAMFontManager(void)
{
	delete bamImp;
}

BAMFontManager::BAMFontManager(void)
{
	isStateFont = false;
	bamImp = new BAMImporter();
	memset(resRef, 0, sizeof(ieResRef));
}

bool BAMFontManager::Open(DataStream* stream)
{
	ieWord len = strlench(stream->filename, '.');
	len = (len <= sizeof(ieResRef)-1) ? len : sizeof(ieResRef)-1;
	strncpy(resRef, stream->filename, len);
	// compare only first 6 chars so we can match states2 or others
	if (strnicmp(resRef, "STATES", 6) == 0) {
		isStateFont = true;
	}
	return bamImp->Open(stream);
}

Font* BAMFontManager::GetFont(unsigned short /*ptSize*/,
							  FontStyle /*style*/, Palette* pal)
{
	AnimationFactory* af = bamImp->GetAnimationFactory(resRef); // released by BAMFont

	Font* fnt = NULL;
	if (isStateFont) {
		// Hack to work around original data where some status icons have inverted x and y positions (ie level up icon)
		// isStateFont is set in Open() and simply compares the first 6 characters of the file with "STATES"

		// since state icons should all be the same size/position we can just take the position of the first one
		Sprite2D* first = af->GetFrame(0, 0);
		int pos = first->YPos; // baseline
		first->release();
		fnt = new BAMFont(af, &pos);
	} else {
		fnt = new BAMFont(af, NULL);
	}

	if (pal) {
		fnt->SetPalette(pal);
	}
	return fnt;
}
