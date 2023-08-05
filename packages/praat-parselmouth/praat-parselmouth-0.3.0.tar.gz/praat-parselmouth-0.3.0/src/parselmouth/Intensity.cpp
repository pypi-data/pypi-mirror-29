/*
 * Copyright (C) 2017-2018  Yannick Jadoul
 *
 * This file is part of Parselmouth.
 *
 * Parselmouth is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Parselmouth is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Parselmouth.  If not, see <http://www.gnu.org/licenses/>
 */

#include "Parselmouth.h"
#include "TimeClassAspects.h"

#include "utils/pybind11/ImplicitStringToEnumConversion.h"
#include "utils/pybind11/Optional.h"

namespace py = pybind11;
using namespace py::literals;

namespace parselmouth {

enum class AveragingMethod {
	MEDIAN = Intensity_averaging_MEDIAN,
	ENERGY = Intensity_averaging_ENERGY,
	SONES = Intensity_averaging_SONES,
	DB = Intensity_averaging_DB
};

PRAAT_ENUM_BINDING(AveragingMethod)

void Binding<AveragingMethod>::init() {
	value("MEDIAN", AveragingMethod::MEDIAN);
	value("ENERGY", AveragingMethod::ENERGY);
	value("SONES", AveragingMethod::SONES);
	value("DB", AveragingMethod::DB);

	make_implicitly_convertible_from_string(*this);
}

void Binding<Intensity>::init() {
	// TODO Get value in frame

	// TODO Mixins (or something else?) for TimeFrameSampled, TimeFunction, and TimeVector functionality

	Bindings<AveragingMethod> subBindings(*this);
	subBindings.init();

	initTimeFrameSampled(*this);

	def("get_value", // TODO Should be part of Vector class
	    [](Intensity self, double time, Interpolation interpolation) { return Vector_getValueAtX(self, time, 1, static_cast<int>(interpolation)); },
	    "time"_a, "interpolation"_a = Interpolation::CUBIC);

	// TODO 'Get mean' should probably also be added to Sampled once units get figured out?

	def("get_average",
	    [](Intensity self, optional<double> fromTime, optional<double> toTime, AveragingMethod averagingMethod) {
		    return Intensity_getAverage(self, fromTime.value_or(self->xmin), toTime.value_or(self->xmax), static_cast<int>(averagingMethod));
	    },
	    "from_time"_a = nullopt, "to_time"_a = nullopt, "averaging_method"_a = AveragingMethod::ENERGY);

	// TODO Pitch_Intensity_getMean & Pitch_Intensity_getMeanAbsoluteSlope ? (cfr. Pitch)
}

} // namespace parselmouth
