import matplotlib.pyplot as plt
import numpy as np
from matplotlib.text import Annotation
from matplotlib.widgets import Slider, CheckButtons, TextBox
from numerical import *
# exact(b, m, k, x, v, t, h)
# euler(b, m, k, x, v, t, h)
# imp_euler(b, m, k, x, v, t, h)
# verlet(b, m, k, x, v, t, h)
# euler_cromer(b, m, k, x, v, t, h)
# chi_sq(y_array, model_array)
# energy(k, x_array, m, v_array)

# Initialise constants.
k0 = 1
m0 = 3
h0 = 0.1
b0 = 0
x0 = 1
v0 = 0

ax_length = 20

t = np.arange(1, ax_length, h0)

# Initialise lines for the graph.
y1 = exact(b0, m0, k0, x0, v0, t, h0)[0]
y2 = euler(b0, m0, k0, x0, v0, t, h0)[0]
y3 = imp_euler(b0, m0, k0, x0, v0, t, h0)[0]
y4 = verlet(b0, m0, k0, x0, v0, t, h0)[0]
y5 = euler_cromer(b0, m0, k0, x0, v0, t, h0)[0]

fig, axx = plt.subplots()

plt.subplots_adjust(left=0.25, bottom=0.3)

line1, = plt.plot(t, y1)
line2, = plt.plot(t, y2)
line3, = plt.plot(t, y3)
line4, = plt.plot(t, y4)
line5, = plt.plot(t, y5)

lines = [line1, line2, line3, line4, line5]

for line in lines:
        line.set_visible(True)

line1.set_label("Exact Solution")
line2.set_label("Euler's Method")
line3.set_label("Improved Euler's Method")
line4.set_label("Verlet's Method")
line5.set_label("Euler-Cromer Method")


# Add checkbuttons to toggle line visibility.
button_ax = plt.axes([0.06, 0.25, 0.15, 0.63])
buttons = CheckButtons(button_ax, [line.get_label() for line in lines],
                       (True, True, True, True, True))


# Add text entry box to allow user to select the force applied.
force_ax = plt.axes([0.06, 0.06, 0.15, 0.08])
time_ax = plt.axes([0.06, 0.15, 0.15, 0.08])

force_box = TextBox(force_ax, "Force:", initial="0")
time_box = TextBox(time_ax, "Time:", initial="0")

# Add slider axes.
axx.legend(loc=1)
axx.set_xlabel("Time")
axx.set_ylabel("Displacement")
b_ax = plt.axes([0.25, 0.06, 0.65, 0.02])
k_ax = plt.axes([0.25, 0.09, 0.65, 0.02])
m_ax = plt.axes([0.25, 0.12, 0.65, 0.02])
h_ax = plt.axes([0.25, 0.15, 0.65, 0.02])
x_ax = plt.axes([0.25, 0.18, 0.65, 0.02])
v_ax = plt.axes([0.25, 0.21, 0.65, 0.02])


# Add annotation on the b slider to show critical levels.

# Critical level.
cr_label = Annotation(s=r"$b_{cr}$", xy=(2 * np.sqrt(k0 * m0), 0),
                      xytext=(2 * np.sqrt(k0 * m0), - 2),
                      arrowprops=dict(arrowstyle='->'))
b_ax.add_artist(cr_label)

# Half-critical level.
cr_label05 = Annotation(s=r"$b_{cr}$", xy=(np.sqrt(k0 * m0), 0),
                        xytext=(np.sqrt(k0 * m0), - 2),
                        arrowprops=dict(arrowstyle='->'))
b_ax.add_artist(cr_label05)

# Twice critical level.
cr_label2 = Annotation(s=r"$b_{cr}$", xy=(4 * np.sqrt(k0 * m0), 0),
                       xytext=(4 * np.sqrt(k0 * m0), - 2),
                       arrowprops=dict(arrowstyle='->'), annotation_clip=False)
b_ax.add_artist(cr_label2)

b_ax.set_xlabel("Arrows show half critical, critical and twice critical "
                "damping levels respectfully.")

k = k0

# Add sliders to alter values.
kslider = Slider(k_ax, 'k', 0, 5, valinit=k0)
mslider = Slider(m_ax, 'm', 0, 5, valinit=m0)
hslider = Slider(h_ax, 'h', 0, 2, valinit=h0)
bslider = Slider(b_ax, 'b', 0, 4, valinit=b0)
xslider = Slider(x_ax, r'$x_0$', 0, 4, valinit=x0)
vslider = Slider(v_ax, r'$v_0$', -4, 4, valinit=v0)


# Energy plot.
fig2 = plt.figure()
plt.xlabel("Time")
plt.ylabel("Energy")

e1 = energy(k0, exact(b0, m0, k0, x0, v0, t, h0)[0], m0,
            exact(b0, m0, k0, x0, v0, t, h0)[1])

e2 = energy(k0, euler(b0, m0, k0, x0, v0, t, h0, 0, 0)[0], m0,
            euler(b0, m0, k0, x0, v0, t, h0, 0, 0)[1])

e3 = energy(k0, imp_euler(b0, m0, k0, x0, v0, t, h0, 0, 0)[0], m0,
            imp_euler(b0, m0, k0, x0, v0, t, h0, 0, 0)[1])

e4 = energy(k0, verlet(b0, m0, k0, x0, v0, t, h0, 0, 0)[0], m0,
            verlet(b0, m0, k0, x0, v0, t, h0, 0, 0)[1])

e5 = energy(k0, euler_cromer(b0, m0, k0, x0, v0, t, h0, 0, 0)[0], m0,
            euler_cromer(b0, m0, k0, x0, v0, t, h0, 0, 0)[1])

energy1, = plt.plot(t, e1)
energy2, = plt.plot(t, e2)
energy3, = plt.plot(t, e3)
energy4, = plt.plot(t, e4)
energy5, = plt.plot(t, e5)

energys = [energy1, energy2, energy3, energy4, energy5]

energy1.set_label("Exact Solution")
energy2.set_label("Euler's Method")
energy3.set_label("Improved Euler's Method")
energy4.set_label("Verlet's Method")
energy5.set_label("Euler-Cromer Method")

for en in energys:
        en.set_visible(True)

fig2.legend()


# Master update function for updating the plotted graphs.
def update(val):
        m = mslider.val
        k = kslider.val
        h = hslider.val
        b = bslider.val
        x = xslider.val
        t = np.arange(1, ax_length, h)
        v = vslider.val
        try:            # Check force and time are valid numbers.
                force = float(force_box.text)
                time = float(time_box.text)
        except:
                force = 0
                time = 0

        # This can be improved aesthetically by, for example, creating a
        # dictionary of relevent functions corresponding to each line,
        # then iterating across the lines calling each function.
        #
        # Potentially a TODO although any performance benefits would be
        # negligible.

        line1.set_ydata(exact(b, m, k, x, v, t, h)[0])
        line1.set_xdata(t)

        line2.set_ydata(euler(b, m, k, x, v, t, h, force=force,
                              time=time)[0])
        line2.set_xdata(t)

        line3.set_ydata(imp_euler(b, m, k, x, v, t, h, force=force,
                                  time=time)[0])
        line3.set_xdata(t)

        line4.set_ydata(verlet(b, m, k, x, v, t, h, force=force, time=time)[0])
        line4.set_xdata(t)

        line5.set_ydata(euler_cromer(b, m, k, x, v, t, h, force=force,
                                     time=time)[0])
        line5.set_xdata(t)

        energy1.set_ydata(energy(k, exact(b, m, k, x, v, t, h)[0], m,
                          exact(b, m, k, x, v, t, h)[1]))
        energy1.set_xdata(t)

        energy2.set_ydata(energy(k, euler(b, m, k, x, v, t, h, force=force,
                                          time=time)[0], m,
                                 euler(b, m, k, x, v, t, h,
                                       force=force, time=time)[1]))
        energy2.set_xdata(t)

        energy3.set_ydata(energy(k, imp_euler(b, m, k, x, v, t, h, force=force,
                                              time=time)[0], m,
                                 imp_euler(b, m, k, x, v, t, h,
                                           force=force,
                                           time=time)[1]))
        energy3.set_xdata(t)

        energy4.set_ydata(energy(k, verlet(b, m, k, x, v, t, h, force=force,
                                           time=time)[0],
                                 m, verlet(b, m, k, x, v, t, h, force=force,
                                 time=time)[1]))
        energy4.set_xdata(t)

        energy5.set_ydata(energy(k, euler_cromer(b, m, k, x, v, t, h,
                                 force=force, time=time)[0], m,
                                 euler_cromer(b, m, k, x, v, t, h, force=force,
                                              time=time)[1]))
        energy5.set_xdata(t)

        # Refresh position of critical damping markers.
        for child in b_ax.get_children():
                if isinstance(child, Annotation):
                        child.remove()

        # TODO This is exactly the same as before. Define as a function.
        cr_label = Annotation(s=r"$b_{cr}$", xy=(2 * np.sqrt(k * m), 0),
                              xytext=(2 * np.sqrt(k * m), -2),
                              arrowprops=dict(arrowstyle='->'))
        b_ax.add_artist(cr_label)

        cr_label05 = Annotation(s=r"$b_{cr}$", xy=(np.sqrt(k * m), 0),
                                xytext=(np.sqrt(k * m), -2),
                                arrowprops=dict(arrowstyle='->'))
        b_ax.add_artist(cr_label05)

        cr_label2 = Annotation(s=r"$b_{cr}$", xy=(4 * np.sqrt(k * m), 0),
                               xytext=(4 * np.sqrt(k * m), -2),
                               arrowprops=dict(arrowstyle='->'),
                               annotation_clip=False)
        b_ax.add_artist(cr_label2)

        # TODO Implement some way of displaying the chi squared between
        # the exact value and the numerical solutions.

        # Refresh both plots
        fig.canvas.draw_idle()
        fig2.canvas.draw_idle()


# TODO Tidy the following: lots of repetition
# Change visibility of plots by flipping their boolean visibility state
def click(label):
        for line in lines:
                if line.get_label() == label:
                        line.set_visible(not line.get_visible())
        for en in energys:
                if en.get_label() == label:
                        en.set_visible(not en.get_visible())
        fig.canvas.draw_idle()
        fig2.canvas.draw_idle()


# Update plots on interaction
buttons.on_clicked(click)
kslider.on_changed(update)
mslider.on_changed(update)
hslider.on_changed(update)
bslider.on_changed(update)
xslider.on_changed(update)
vslider.on_changed(update)
force_box.on_submit(update)
time_box.on_submit(update)
fig.canvas.set_window_title("Approximations for SHM")
fig2.canvas.set_window_title("Energy")
plt.show()
