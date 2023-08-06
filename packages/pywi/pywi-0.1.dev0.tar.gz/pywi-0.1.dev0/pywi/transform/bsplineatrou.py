#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# See http://localhost:8888/notebooks/signal_processing_wavelet_transform_fr.ipynb

# Tool functions

def read_fits_file(file_path):
    hdu_list = fits.open(file_path) # Open the FITS file
    data = hdu_list[0].data
    hdu_list.close()                # Close the FITS file
    return data

def plot(data, title="", cmap="gnuplot2"):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    im = ax.imshow(data, interpolation='nearest', origin='lower', cmap=cmap)   # cmap=cm.inferno and cmap="inferno" are both valid
    ax.set_title(title)

    plt.colorbar(im) # draw the colorbar
    plt.show()

def get_pixel_value(image, x, y, type_border):
    if type_border == 0:
        try:
            pixel_value = image[x, y]
            return pixel_value
        except IndexError as e:
            return 0
    elif type_border == 1:
        num_lines, num_col = image.shape    # TODO
        x = x % num_lines
        y = y % num_col
        pixel_value = image[x, y]
        return pixel_value
    elif type_border == 2:
        num_lines, num_col = image.shape    # TODO

        if x >= num_lines:
            x = num_lines - 2 - x
        elif x < 0:
            x = abs(x)

        if y >= num_col:
            y = num_col - 2 - y
        elif y < 0:
            y = abs(y)

        pixel_value = image[x, y]
        return pixel_value
    elif type_border == 3:
        num_lines, num_col = image.shape    # TODO

        if x >= num_lines:
            x = num_lines - 1 - x
        elif x < 0:
            x = abs(x) - 1

        if y >= num_col:
            y = num_col - 1 - y
        elif y < 0:
            y = abs(y) - 1

        pixel_value = image[x, y]
        return pixel_value
    else:
        raise ValueError()

def smooth_bspline(input_image, type_border, step_trou):
#    int num_lines = img_in.nl();  // num lines in the image
#    int num_col = img_in.nc();  // num columns in the image
#
#    int i, j, step;
#
#    float coeff_h0 = 3. / 8.;
#    float coeff_h1 = 1. / 4.;
#    float coeff_h2 = 1. / 16.;
#
#    Ifloat buff(num_lines, num_col, "buff smooth_bspline");
#
#    step = (int)(pow((double)2., (double) step_trou) + 0.5);
#
#    for (i = 0; i < num_lines; i ++)
#    for (j = 0; j < num_col; j ++)
#       buff(i,j) = coeff_h0 * img_in(i,j)
#                 + coeff_h1 * (  img_in(i, j-step, type_border)
#                               + img_in(i, j+step, type_border))
#                 + coeff_h2 * (  img_in(i, j-2*step, type_border)
#                               + img_in(i, j+2*step, type_border));
#
#    for (i = 0; i < num_lines; i ++)
#    for (j = 0; j < num_col; j ++)
#       img_out(i,j) = coeff_h0 * buff(i,j)
#                    + coeff_h1 * (  buff(i-step, j, type_border)
#                                  + buff(i+step, j, type_border))
#                    + coeff_h2 * (  buff(i-2*step, j, type_border)
#                                  + buff(i+2*step, j, type_border));

    input_image = input_image.astype('float64', copy=True)

    coeff_h0 = 3. / 8.
    coeff_h1 = 1. / 4.
    coeff_h2 = 1. / 16.

    num_lines, num_col = input_image.shape    # TODO

    buff = np.zeros(input_image.shape, dtype='float64')
    img_out = np.zeros(input_image.shape, dtype='float64')

    step = int(pow(2., step_trou) + 0.5)

    #print("step =", step)

    for i in range(num_lines):
        for j in range(num_col):
            buff[i,j]  = coeff_h0 *    get_pixel_value(input_image, i, j,        type_border)
            buff[i,j] += coeff_h1 * (  get_pixel_value(input_image, i, j-step,   type_border) \
                                     + get_pixel_value(input_image, i, j+step,   type_border))
            buff[i,j] += coeff_h2 * (  get_pixel_value(input_image, i, j-2*step, type_border) \
                                     + get_pixel_value(input_image, i, j+2*step, type_border))

#    for (i = 0; i < num_lines; i ++)
#    for (j = 0; j < num_col; j ++)
#       img_out(i,j) = coeff_h0 * buff(i,j)
#                    + coeff_h1 * (  buff(i-step, j, type_border)
#                                  + buff(i+step, j, type_border))
#                    + coeff_h2 * (  buff(i-2*step, j, type_border)
#                                  + buff(i+2*step, j, type_border));
    for i in range(num_lines):
        for j in range(num_col):
            img_out[i,j]  = coeff_h0 *    get_pixel_value(buff, i,        j, type_border)
            img_out[i,j] += coeff_h1 * (  get_pixel_value(buff, i-step,   j, type_border) \
                                        + get_pixel_value(buff, i+step,   j, type_border))
            img_out[i,j] += coeff_h2 * (  get_pixel_value(buff, i-2*step, j, type_border) \
                                        + get_pixel_value(buff, i+2*step, j, type_border))

    return img_out

def transform(image, num_scales):
    # MR_Transf.band(0) = Image;
    # for (s = 0; s < Nbr_Plan -1; s++)
    # {
    #     smooth_bspline (MR_Transf.band(s),MR_Transf.band(s+1),Border,s);
    #     if  (Details == True) MR_Transf.band(s) -= MR_Transf.band(s+1);
    # }

    image = image.astype('float64', copy=True)

    scale_list = []
    scale_list.append(image)

    for scale_index in range(num_scales - 1):
        previous_scale = scale_list[scale_index]

        next_scale = smooth_bspline(previous_scale, 3, scale_index)

        previous_scale -= next_scale

        scale_list.append(next_scale)

    return scale_list
