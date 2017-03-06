package podcast.services;

import com.couchbase.client.java.Bucket;
import com.couchbase.client.java.document.JsonDocument;
import com.couchbase.client.java.document.json.JsonObject;
import com.couchbase.client.java.query.N1qlQuery;
import com.couchbase.client.java.query.N1qlQueryRow;
import org.codehaus.jackson.JsonNode;
import org.springframework.stereotype.Service;
import podcast.models.entities.Session;
import podcast.models.entities.User;
import java.util.List;
import java.util.Optional;

/**
 * Service to handle storage and querying of
 * user information in Couchbase
 */
@Service
public class UsersService {

  /**
   * Store a user
   * @param bucket - Bucket
   * @param user - User
   */
  private void storeUser(Bucket bucket, User user) {
    bucket.upsert(JsonDocument.create(user.getUuid(), user.toJsonObject()));
  }


  /**
   * Create a user based on a response from Google Sign In
   * @param bucket - Bucket
   * @param response - JsonNode
   */
  public User createUser(Bucket bucket, JsonNode response) {
    User user = new User(response);
    user.setSession(new Session(user));
    storeUser(bucket, user);
    return user;
  }


  /**
   * Get User by Google ID
   * @param bucket - Bucket
   * @param googleID - String
   * @return - Optional User
   * @throws Exception - if dups
   */
  public Optional<User> getUserByGoogleID(Bucket bucket, String googleID) {
    // Prepare and execute N1QL query

    JsonObject placeholderValues = JsonObject.create().put("googleID", googleID);
    N1qlQuery q = N1qlQuery.simple("SELECT * FROM `users` where googleID='" + googleID + "'");
    List<N1qlQueryRow> rows = bucket.query(q).allRows();

    // If empty
    if (rows.size() == 0) {
      return Optional.empty();
    }

    // Grab the user accordingly
    return Optional.of(new User(rows.get(0).value().getObject("users")));
  }


}
