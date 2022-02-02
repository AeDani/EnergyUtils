from profile import Profile
import matplotlib.pyplot as plt


myProfile = Profile.random_profile('2021-01-01 00:00', '2021-12-31 23:00')
print(len(myProfile.values))
myProfile.values.plot()
plt.show()
