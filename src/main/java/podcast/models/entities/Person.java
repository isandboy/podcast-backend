package podcast.models.entities;

import lombok.Getter;

/** Person scopes down the fields in User **/
public class Person {

  @Getter private String id;
  @Getter private String firstName;
  @Getter private String lastName;
  @Getter private String username;
  @Getter private Integer numberFollowers;
  @Getter private Integer numberFollowing;
  @Getter private String imageUrl;

  public Person(User user) {
    this.id = user.getId();
    this.firstName = user.getFirstName();
    this.lastName = user.getLastName();
    this.username = user.getUsername();
    this.numberFollowers = user.getNumberFollowers();
    this.numberFollowing = user.getNumberFollowing();
    this.imageUrl = user.getImageUrl();
  }

}
