fig = plt.figure()
ax = plt.axes(xlim =(-4E8,4E8), ylim= (-4E8,4E8))
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)

def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])

        pt.set_data([], [])
        time_text.set_text('hello')
    return lines + pts + [time_txt,]

def animate(i):
    i = (10 * i) % data.shape[1]
    #update lines and points here
    for line, pt, dt in zip(lines,pts, data):
        x, y, z = dt[:i].T
        line.set_data(x, y)

        pt.set_data(x[-1:], y[-1:])

        time_text.set_text('time = %.1d' % i) #<<<<<Here. This doesn't work
    return lines + pts + [time_txt,]

anim = animation.FuncAnimation(fig, animate, init_func=init,
                           frames=700, interval=1, blit=True)
plt.show()
